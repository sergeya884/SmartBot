import serial
from tkinter import *

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

# Подключаем порт с arduino
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

# Создаем окно с элементами управления   
root=Tk()
root.title('main')

# Задаем управление с клавиатуры
root.bind("<w>", go_forward)
root.bind("<s>", go_back)
root.bind("<a>", turn_left)
root.bind("<d>", turn_right)
root.bind("<g>", tower_left)
root.bind("<h>", tower_right)
root.bind("<space>", stop)
root.bind("<f>", fire)

# Зацикливаем
root.mainloop()
