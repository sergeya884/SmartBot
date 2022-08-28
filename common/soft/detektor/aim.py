import cv2
import serial
import time
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

# Функция-поток контроля попадания ==========================================
def fire_control():
    
    # Временной интервал, необходимый для перезарядки орудия
    interval = 7
    # i - счетчик времени
    i = interval
    
    while True :
        # Проверка выполняется раз в секунду
        time.sleep(1)
        i+=1
        if i > interval: i = interval
  
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

# Запускаем процесс контроля попадания
process_fire_control = Thread(target=fire_control, args=())
process_fire_control.start()

while True:
    # Получаем картинку и переводим в чб 320х240
    success, img = cap.read()
    img = cv2.resize(img, (320, 240))
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
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
                
    # Выводим картинку
    cv2.imshow('name of window', img) 
    
    if cv2.waitKey(1) & 0xff == ord('q'):  break
# Завершаем все процессы
cap.release()
ser.write(b"s\n") 
cv2.destroyAllWindows() 
