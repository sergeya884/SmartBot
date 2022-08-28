'''
В программе запускается 3 параллельных процесса. Основной получает видео поток и может наводится на мишень, второй поток отвечает за ручное управление и третий контралирует попадания.
'''

import serial
import time
from tkinter import *
from PIL import Image, ImageTk
import cv2
from threading import Thread

# Функция для трансляции видео с камеры =====================================
def gstreamer_pipeline(sensor_id=0, capture_width=1640, capture_height=1232, display_width=320, display_height=240, framerate=10, flip_method=0, ):
    return (
        "nvarguscamerasrc sensor-id=%d ! "
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink "
        % ( sensor_id, capture_width, capture_height, framerate, flip_method, display_width,display_height, )
    )

# Функция-поток ручного управления роботом =================================
def control():

    # Функции, срабатывающие при нажатии на клавиши ------------------------
    # Функции управления движением, задают направление и скорость
    def go_forward(a): ser.write(b"g\n1 255\n")
    def go_back(a):    ser.write(b"g\n2 255\n")
    def turn_left(a):  ser.write(b"g\n3 255\n")
    def turn_right(a): ser.write(b"g\n4 255\n")

    # Функция "остановить все"
    def stop(a): ser.write(b"s\n")
    # Фунуция "огонь"
    def fire(a): ser.write(b"f\n")
    
    # Функции поворота башни, задают направление и скорость
    def tower_left(a):  ser.write(b"t\n1 200\n")
    def tower_right(a): ser.write(b"t\n2 200\n")
    
    # Функция управления манипулятором 
    def manip(i, var):
        # Формируем команду, m - "управление манипулятором", i - степень свободы, angle - угол
        string = "m\n" + str(i) + " " + str(var) + "\n"
        # Отправляем байтами
        ser.write(string.encode('utf-8'))
        
    # Задаем нажатия на клавиши --------------------------------------------
    # Создаем окно с элементами управления   
    root = Tk()
    root.title('main')
    root.attributes('-zoomed', True)
    
    # Задаем управление с клавиатуры
    root.bind("<w>", go_forward)
    root.bind("<s>", go_back)
    root.bind("<a>", turn_left)
    root.bind("<d>", turn_right)
    root.bind("<g>", tower_left)
    root.bind("<h>", tower_right)
    root.bind("<space>", stop)
    root.bind("<f>", fire)
    
    # Выводим видео с камеры на экран --------------------------------------
    # Конвертируем Image object в TkPhoto object
    im = Image.fromarray(img)
    imgtk = ImageTk.PhotoImage(image=im) 
   
    # Выводим картинку на экран
    panel = Label(root, image=imgtk)
    panel.pack()

    # Функция обновления карьинки. 
    def callback():
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im) 
        panel.configure(image=imgtk)
        panel.image = imgtk
        root.after(200, callback)
    callback()
    
    # Задаем ползунки управления манипулятором -----------------------------
    # Задаем ползунки для управления степенями свободы
    scale0 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1,  command=lambda value: manip(0, value), font=('sans-serif', 14)) 
    
    scale1 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1,  command=lambda value: manip(1, value), font=('sans-serif', 14))
    
    scale2 = Scale(root, orient=HORIZONTAL, length=200, from_=40, to=120, resolution=1,     command=lambda value: manip(2, value), font=('sans-serif', 14)) 
    
    scale3 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1,  command=lambda value: manip(3, value), font=('sans-serif', 14)) 
    
    scale4 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1,  command=lambda value: manip(4, value), font=('sans-serif', 14)) 
    
    scale5 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1,  command=lambda value: manip(5, value), font=('sans-serif', 14)) 
    
    scale6 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1,  command=lambda value: manip(6, value), font=('sans-serif', 14)) 
    
    # Включаем отоброжение ползунков
    scale0.pack() 
    scale1.pack() 
    scale2.pack() 
    scale3.pack() 
    scale4.pack() 
    scale5.pack() 
    scale6.pack() 
    
    # Задаем начальные положения ползунков и сервоприводов манипулятора
    scale0.set(90)
    manip(0, 90)
    scale1.set(10)
    manip(1, 10)
    scale2.set(70)
    manip(2, 70)
    scale3.set(90)
    manip(3, 90)
    scale4.set(0)
    manip(4, 0)
    scale5.set(90)
    manip(5, 90)
    scale6.set(90)
    manip(6, 90)
    
    # Задаем кнопку управления патрулем ------------------------------------
    def patrol_control(): 
        global patrol
        if patrol == False: 
            patrol = True
            patrol_btn['text'] = 'ОСТАНОВИТЬ ПАТРУЛЬ'
        else: 
            patrol = False
            patrol_btn['text'] = 'НАЧАТЬ ПАТРУЛЬ'
        
    patrol_btn = Button(text = 'НАЧАТЬ ПАТРУЛЬ', command = patrol_control)
    patrol_btn.pack()
    
    # -----------------------------------------------------------------------
    # Зацикливаем
    root.mainloop()  
    
    # После закрытия окна даем команду завершить все процессы
    global Open
    Open = False 

# Функция-поток контроля попадания ==========================================
def fire_control():
    global Open
    global patrol
    
    # Временной интервал, необходимый для перезарядки орудия
    interval = 7
    # i - счетчик времени
    i = interval
    
    # Пока окно не закрыли
    while Open == True :
        # Проверка выполняется раз в секунду
        time.sleep(1)
        i+=1
        if i > interval: i = interval
        
        # Если пришла команда начать патруль 
        if patrol == True:
            # Находим мишень
            for (x, y, w, h) in faces:       
                # Если мишень в центре кадра, стреляем и обнуляем счетчик
                if  (150 < x+w//2 < 170) and (i >= interval): 
                    ser.write(b"f\n")
                    i = 0
            # Останавливаем башню, чтобы в случае потери мишени 
            # она не продолжала движения
            ser.write(b"t\n1 0\n")
            ser.write(b"t\n2 0\n")

# Основной поток ============================================================
# Подключаем порт с arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

# Подключаем модель обученного каскада haara
face_cascade_db = cv2.CascadeClassifier("tank.xml") 
cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)   

# Досылаем первый патрон
time.sleep(1)
ser.write(b"m\n7 180\n")
time.sleep(0.6)
ser.write(b"m\n7 0\n")

# Переменная, отвечающая за своевременное завершение всех процессов 
global Open
Open = True
# Переменная, отвечающая за начало и конец патруля 
global patrol
patrol = False

# Запускаем процесс ручного управления
process_control = Thread(target=control, args=())
process_control.start()

# Запускаем процесс контроля попадания
process_fire_control = Thread(target=fire_control, args=())
process_fire_control.start()

# Если окно оькрыто
while Open == True:
    # Получаем картинку и переводим в чб 320х240
    success, img = cap.read()
    img = cv2.resize(img, (320, 240))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Если пришла команда начать патруль 
    if patrol == True :
        # Находим мишень    
        faces = face_cascade_db.detectMultiScale(img_gray, 1.1, 50, 0)
        for (x, y, w, h) in faces:       
            
            # Рисуем прямоугольник
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
            
            # Наводимся. Скорость поворота башни зависит от растояния до центра экрана.
            if (x+w//2 <=  100):           ser.write(b"t\n1 255\n")
            elif (100 <= x+w//2 <=  140):  ser.write(b"t\n1 200\n")
            elif (140 <= x+w//2 <=  150): ser.write(b"t\n1 150\n")
            elif (220 <= x+w//2 ):        ser.write(b"t\n2 255\n")
            elif (180 <= x+w//2 <=  220): ser.write(b"t\n2 200\n")
            elif (170 <= x+w//2 <=  180): ser.write(b"t\n2 150\n")
            else: 
                ser.write(b"t\n1 0\n")
                ser.write(b"t\n2 0\n")

# Завершаем все процессы
cap.release()
ser.write(b"s\n") 
cv2.destroyAllWindows() 
