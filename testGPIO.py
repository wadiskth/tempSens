import os, glob, sys, time
import RPi.GPIO as GPIO

from tempSensing import Temp
from mediaScanner import *
from arduino_connection import ArduinoConnection
from time import strftime
from datetime import datetime

GPIO.setmode(GPIO.BCM)
GPIO.setup(31, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(30, GPIO.IN, pull_up_down = GPIO.PUD_UP)
def Int_shutdown1(channel):
    print 'wheee!'

def Int_shutdown2(channel):
    print 'whooo!'

GPIO.add_event_detect(30, GPIO.FALLING, callback = Int_shutdown1, bouncetime = 2000)
GPIO.add_event_detect(31, GPIO.FALLING, callback = Int_shutdown2, bouncetime = 2000)

arduinoAnalog=ArduinoConnection()
arduinoAnalog.start()

wortTemp=Temp(fileName='28-0000057a672b')
wortTemp.start()

while 1:
    time.sleep(1)
    print 'in za loop!'
