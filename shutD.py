import os
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(31, GPIO.IN, pull_up_down = GPIO.PUD_UP)
def Int_shutdown(channel):
    os.system('sudo shutdown -h now')
    
GPIO.add_event_detect(31, GPIO.FALLING, callback = Int_shutdown, bouncetime = 2000)

while 1:
    time.sleep(1)
