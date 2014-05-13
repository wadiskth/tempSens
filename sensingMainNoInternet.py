import os, glob, sys, time
import RPi.GPIO as GPIO

from tempSensing import Temp
from mediaScanner import *
from arduino_connection import ArduinoConnection
from time import strftime
from datetime import datetime



os.system('modprobe w1-gpio');
os.system('modprobe w1-therm');
    # init interrupt
GPIO.setmode(GPIO.BCM)
GPIO.setup(31, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(30, GPIO.IN, pull_up_down = GPIO.PUD_UP)


def write_and_verify(fileName,data):
    print 'Writing to file: ', fileName
    f = file(fileName,'a')
    f.write(data)
    f.write('\n')
    f.flush()
    os.fsync(f.fileno())
    f.close()
    f = file(fileName,'r')
    verified = f.read()
    f.close()
    return  verified == data and f.closed


def get_partition(dev):
    print 'Getting partiton : ', dev
    os.system('fdisk -l %s > output' % dev)
    f = file('output')
    data = f.read()
    f.close()
    return data.split('\n')[-2].split()[0].strip()


def mount_partition(partition):
    os.system('mount %s /media/usb0' % partition)


def unmount_partition():
    os.system('umount /media/usb0')


def get_date():
    # get date
    _date = strftime('%D', time.localtime())
    return _date


def get_time():
    # get time
    _time = strftime('%H:%M:%S', time.localtime())
    return _time        

def writeToFile(values, fName):
    values = SEPARATOR.join(map(str,values))
    try:
        write_and_verify(fName, values)
    except:
        print 'could not write to file!'
    

def writeValues(values, toFile, fName):
    if toFile:
        writeToFile(values, fName)
        

def initDevices():
    # mount devices -----------------------
    ms = MediaScanner()
    devices = ms.scan_media()
    print 'Devices :', devices
    #if devices:
     #   for device in devices:
      #      mount_partition(get_partition(device))

def getFileName():
    maxFileName = 0
    currentFile = 0
    folderRoot = '/media/usb0/'
    fileType = '.csv'
    for filename in os.listdir(folderRoot):
        if filename.lower().endswith('.csv'):
            try:
                currentFile = int(os.path.splitext(filename)[0])
                if currentFile > maxFileName:
                    maxFileName = currentFile
            except ValueError:
                print 'File name ' + str(filename) + ' not within naming conventions.'
    currentFile = currentFile + 1
    return folderRoot + str(currentFile) + fileType

def Int_shutdown(channel):
    print '31'
    #os.system('sudo shutdown -h now')

def Int_pause(channel):
    print '30'
    #if pause:
    #    pause = False
    #else:
    #    pause = True


    # Static variable init *********************** 
arduinoAnalogValues = [0.0] * 6
allValuesArray = [0.0] * 9
flag = True
SEPARATOR = ';'
flagWriteToFile = True
fileName = ''
pause = False

GPIO.add_event_detect(31, GPIO.FALLING, callback = Int_shutdown, bouncetime = 2000)
GPIO.add_event_detect(30, GPIO.FALLING, callback = Int_pause, bouncetime = 2000)

    # init devices
initDevices()

    # init threads ***********************
        # init arduino thread -----------------------
arduinoAnalog=ArduinoConnection()
arduinoAnalog.start()
        # replace tempId with the id of your temperature probe. inits the gpio pins. -----------------------
       
wortTemp=Temp(fileName='28-0000057a672b')
wortTemp.start()

print 'Start date is: ', get_date(), get_time()

fileName = getFileName()

while (flag):

    if pause:
        print 'pause'
        fileName = getFileName()
    else:
        print 'run'
        arduinoAnalogValues = arduinoAnalog.getMeanAnalogArduinoValueArray()
    
        allValuesArray[0] = get_date();
        allValuesArray[1] = get_time();
        allValuesArray[2] = wortTemp.getCurrentTemp();
        allValuesArray[3] = arduinoAnalogValues[0];
        allValuesArray[4] = arduinoAnalogValues[1];
        allValuesArray[5] = arduinoAnalogValues[2];
        allValuesArray[6] = arduinoAnalogValues[3];
        allValuesArray[7] = arduinoAnalogValues[4];
        allValuesArray[8] = arduinoAnalogValues[5];
        
        writeValues(allValuesArray, flagWriteToFile, fileName)
    
    time.sleep(5)
unmount_partition()
