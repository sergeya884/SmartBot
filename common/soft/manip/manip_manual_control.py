import serial
from tkinter import *

# Функция управления манипулятором
def manip(i, angle):
    # Формируем команду, m - "управление манипулятором", i - степень свободы, angle - угол
    string = "m\n" +str(i)+ " "+ str(angle) + "\n"
    # Отправляем байтами
    ser.write(string.encode('utf-8'))
    
# Подключаем порт с arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

# Создаем окно с элементами управления
root=Tk()
root.title('manip')

# Задаем ползунки для управления степенями свободы
scale0 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1, command=lambda value: manip(0, value), font=('sans-serif', 14)) 

scale1 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1, command=lambda value: manip(1, value), font=('sans-serif', 14))

scale2 = Scale(root, orient=HORIZONTAL, length=200, from_=40, to=120, resolution=1, command=lambda value: manip(2, value), font=('sans-serif', 14)) 

scale3 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1, command=lambda value: manip(3, value), font=('sans-serif', 14)) 

scale4 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1, command=lambda value: manip(4, value), font=('sans-serif', 14)) 

scale5 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1, command=lambda value: manip(5, value), font=('sans-serif', 14)) 

scale6 = Scale(root, orient=HORIZONTAL, length=200, from_=0, to=180, resolution=1, command=lambda value: manip(6, value), font=('sans-serif', 14)) 

# Включаем отоброжение ползунков
scale0.pack() 
scale1.pack() 
scale2.pack() 
scale3.pack() 
scale4.pack() 
scale5.pack() 
scale6.pack() 

# Задаем начальные положения
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

# Зацикливаем
root.mainloop()
