from tkinter import Tk, Label
import RPi.GPIO as GPIO
import time

# Pin Definitions
motor_pin_r_f = 12  
motor_pin_r_b = 11  
motor_pin_l_f = 16  
motor_pin_l_b = 15  

def go_forward(a):
    GPIO.output(motor_pin_r_b, GPIO.LOW)
    GPIO.output(motor_pin_l_b, GPIO.LOW)
    GPIO.output(motor_pin_r_f, GPIO.HIGH)
    GPIO.output(motor_pin_l_f, GPIO.HIGH)
def go_back(a):
    GPIO.output(motor_pin_r_f, GPIO.LOW)	
    GPIO.output(motor_pin_l_f, GPIO.LOW)
    GPIO.output(motor_pin_r_b, GPIO.HIGH)
    GPIO.output(motor_pin_l_b, GPIO.HIGH)
def turn_left(a):
    GPIO.output(motor_pin_r_f, GPIO.LOW)
    GPIO.output(motor_pin_l_b, GPIO.LOW)
    GPIO.output(motor_pin_l_f, GPIO.HIGH)
    GPIO.output(motor_pin_r_b, GPIO.HIGH)
def turn_right(a):
    GPIO.output(motor_pin_l_f, GPIO.LOW)
    GPIO.output(motor_pin_r_b, GPIO.LOW)
    GPIO.output(motor_pin_r_f, GPIO.HIGH)
    GPIO.output(motor_pin_l_b, GPIO.HIGH)
def stop(a):
    GPIO.output(motor_pin_l_f, GPIO.LOW)
    GPIO.output(motor_pin_l_b, GPIO.LOW)
    GPIO.output(motor_pin_r_f, GPIO.LOW)
    GPIO.output(motor_pin_r_b, GPIO.LOW)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(motor_pin_l_f, GPIO.OUT)
GPIO.setup(motor_pin_l_b, GPIO.OUT)
GPIO.setup(motor_pin_r_f, GPIO.OUT)
GPIO.setup(motor_pin_r_b, GPIO.OUT)
GPIO.setup(motor_pin_r_b, GPIO.OUT)

root=Tk()
root.bind("<w>", go_forward)
root.bind("<s>", go_back)
root.bind("<a>", turn_left)
root.bind("<d>", turn_right)
root.bind("<space>", stop)
root.mainloop()
