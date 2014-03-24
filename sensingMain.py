
from tempSensing import Temp
from mediaScanner import *
import time
from time import strftime
from datetime import datetime

import os, glob, sys, gspread 

os.system('modprobe w1-gpio');
os.system('modprobe w1-therm');

def write_and_verify(fileName,data):
    print str('Writing to file: ')
    print fileName
    #with open(fileName, "a") as myfile:
    #myfile.write(data)
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
    print str('Getting partiton : ')
    print dev
    os.system('fdisk -l %s > output' % dev)
    f = file('output')
    data = f.read()
    print str('Partition data')
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

def get_first_empty_cell():
    i = 1
    while i < worksheet.row_count:
        print i
        print worksheet.cell(i,1)
        if worksheet.cell(i,1).value==None:
	    return i;
	i = i+1

def increase_ws_size(k):
   if k > worksheet.row_count:
	worksheet.resize(worksheet.row_count*2);

#Google account details
email = 'WADIS.KTH@gmail.com'
password = '23032014KTH'
spreadsheet = 'Temperature_log' #the name of the spreadsheet already created
 
#attempt to log in to your google account
try:
   gc = gspread.login(email,password)
except:
    print('fail')
    sys.exit()
 
#open the spreadsheet
worksheet = gc.open(spreadsheet).sheet1

#replace tempId with the id of your temperature probe, inits the gpio pins.
wortTemp=Temp(fileName='28-0000057a672b')
wortTemp.start()    

ms = MediaScanner()
devices = ms.scan_media()

print 'Start date is: ', get_date(), get_time()

print str('Devices :')
print devices

if devices:
    for device in devices:
        mount_partition(get_partition(device))
#the rest of your code is below. 
# The Temp class will be updating on its own thread which will allow you to do 
#  anything you want on the main thread.
flag = True;
k = get_first_empty_cell();
print (str("this is k"))
print k
worksheet.resize(5,3) 
while (flag ):
    print str("Current temprature :")
    print str(wortTemp.getCurrentTemp())
    values = str(get_date()) + ',' + str(get_time()) + ',' + str(wortTemp.getCurrentTemp())
    write_and_verify('/media/usb0/temp_.csv', values)
    worksheet.update_cell(k,1,get_date())
    worksheet.update_cell(k,2,str(get_time()))
    worksheet.update_cell(k,3, str(wortTemp.getCurrentTemp()))
    k = k +1
    increase_ws_size(k);
    time.sleep(3)
unmount_partition()













