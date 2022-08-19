import RPi.GPIO as GPIO
import time

# Pin Definitions
motor_pin_r_f = 12  # BOARD pin 12, BCM pin 18
motor_pin_r_b = 16  # BOARD pin 16, BCM pin 23
motor_pin_l_f = 15  # BOARD pin 15, BCM pin 22
motor_pin_l_b = 18  # BOARD pin 18, BCM pin 24

def go_forward():
	GPIO.output(motor_pin_r_b, GPIO.LOW)
	GPIO.output(motor_pin_l_b, GPIO.LOW)
	GPIO.output(motor_pin_r_f, GPIO.HIGH)
	GPIO.output(motor_pin_l_f, GPIO.HIGH)
def go_back():
	GPIO.output(motor_pin_r_f, GPIO.LOW)	
	GPIO.output(motor_pin_l_f, GPIO.LOW)
	GPIO.output(motor_pin_r_b, GPIO.HIGH)
	GPIO.output(motor_pin_l_b, GPIO.HIGH)
def turn_left():
	GPIO.output(motor_pin_r_f, GPIO.LOW)
	GPIO.output(motor_pin_l_b, GPIO.LOW)
	GPIO.output(motor_pin_l_f, GPIO.HIGH)
	GPIO.output(motor_pin_r_b, GPIO.HIGH)
def turn_right():
	GPIO.output(motor_pin_l_f, GPIO.LOW)
	GPIO.output(motor_pin_r_b, GPIO.LOW)
	GPIO.output(motor_pin_r_f, GPIO.HIGH)
	GPIO.output(motor_pin_l_b, GPIO.HIGH)
def stop():
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

go_forward()
time.sleep(1)
go_back()
time.sleep(1)
turn_right()
time.sleep(1)
turn_left()
time.sleep(1)
stop()

GPIO.cleanup()
