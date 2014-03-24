from tempSensing import Temp
from mediaScanner import *
import time
import datetime
#replace tempId with the id of your temperature probe, inits the gpio pins.
os.system('modprobe w1-gpio');
os.system('modprobe w1-therm');

wortTemp=Temp(fileName='28-0000057a672b')
wortTemp.start()

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

ms = MediaScanner()
devices = ms.scan_media()
print str('Devices :')
print devices

if devices:
    for device in devices:
        mount_partition(get_partition(device))
#the rest of your code is below. 
# The Temp class will be updating on its own thread which will allow you to do 
#  anything you want on the main thread.
flag = True;
while (flag ):
    k = 0; 
    print str("Current temprature :")
    print str(wortTemp.getCurrentTemp())
    write_and_verify('/media/usb0/temp.txt', str(wortTemp.getCurrentTemp()))
    time.sleep(5)
    k = k+1
    if k == 20:
        flag = False
unmount_partition()

