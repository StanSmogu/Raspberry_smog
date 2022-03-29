import RPi.GPIO as GPIO
from time import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
GPIO.setup(21, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.output(21, GPIO.LOW)
GPIO.output(20, GPIO.LOW)
GPIO.output(16, GPIO.LOW)
while True:
    GPIO.output(21, GPIO.HIGH)
    sleep(0.2)
    GPIO.output(20, GPIO.HIGH)
    sleep(0.2)
    GPIO.output(16, GPIO.HIGH)
    sleep(0.2)
    GPIO.output(21, GPIO.LOW)
    sleep(0.2)
    GPIO.output(20, GPIO.LOW)
    sleep(0.2)
    GPIO.output(16, GPIO.LOW)
    sleep(0.2)
   