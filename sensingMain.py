import os, glob, sys, gspread, time

from tempSensing import Temp
from mediaScanner import *
from arduino_connection import ArduinoConnection
from time import strftime
from datetime import datetime


os.system('modprobe w1-gpio');
os.system('modprobe w1-therm');


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


def get_first_empty_cell(worksheet):
    i = 1
    print 'total worksheet row count: ' + str(worksheet.row_count)
    while i < worksheet.row_count:
        print str(worksheet.cell(i,1).value==None)
        if worksheet.cell(i,1).value==None:
            print 'worksheet.cell(i,1).value: ' + str(worksheet.cell(i,1).value)
            print 'first empty row: ' + str(i)
	    return i;	
	i = i+1
	print 'default empty row: ' + str(i)
    return (i+1)

def increase_ws_size(worksheet, k):
   if k > worksheet.row_count:
	worksheet.resize(worksheet.row_count*2);

def writeToInternet(values, worksheet, k):
    try:
       for i in range(len(values)):
           worksheet.update_cell(k,i+1,values[i])
    except:
        print 'worksheet faild to update!'
    try:
        increase_ws_size(worksheet, k+1);
    except:
        print "Couldnt resize the worksheet"
        

def writeToFile(values):
    values = SEPARATOR.join(map(str,values))
    try:
        write_and_verify('/media/usb0/temp.csv', values)
    except:
        print 'could not write to file!'
    

def writeValues(values, worksheet, k, flagWriteToFile, flagWriteToInternet):
    if flagWriteToInternet:
        writeToInternet(values, worksheet, k)
    if flagWriteToFile:
        writeToFile(values)

def initSpreadsheetConnection():
    # Google account details -----------------------
    email = 'WADIS.KTH@gmail.com'
    password = '23032014KTH'
    #the name of the spreadsheet already created
    spreadsheet = 'Temperature_log'

    worksheet = None
    
    if flagWriteToInternet:    
        # attempt to log in to your google account -----------------------
        try:
            gc = gspread.login(email,password)
        except:
            print('failed to login to email') 
            # open the spreadsheet -----------------------
        try:
            worksheet = gc.open(spreadsheet).sheet1
        except:
            print 'failed to open the spreadsheet'
    return worksheet


def initDevices():
    # mount devices -----------------------
    ms = MediaScanner()
    devices = ms.scan_media()
    print 'Devices :', devices
    if devices:
        for device in devices:
            mount_partition(get_partition(device))


    # Static variable init *********************** 
arduinoAnalogValues = [0.0] * 6
allValuesArray = [0.0] * 9
flag = True
SEPARATOR = ';'
k = 1
flagWriteToFile = False
flagWriteToInternet = False
worksheet = None


    # init internet connection
try:
    worksheet = initSpreadsheetConnection()
except:
    print 'internet connection not established!'


    # init devices
initDevices()


    # Function variable init ***********************
        # get first cell -----------------------
if flagWriteToInternet:
    try:
        k = get_first_empty_cell(worksheet)
    except:
        print 'could not get first empty cell!'


    # init threads ***********************
        # init arduino thread -----------------------
arduinoAnalog=ArduinoConnection()
arduinoAnalog.start()
        # replace tempId with the id of your temperature probe. inits the gpio pins. -----------------------
wortTemp=Temp(fileName='28-0000057a672b')
wortTemp.start()


print 'Start date is: ', get_date(), get_time()


while (flag ):
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
    
    writeValues(allValuesArray, worksheet, k, flagWriteToFile, flagWriteToInternet)
    
    k = k + 1
    
    time.sleep(5)
unmount_partition()
