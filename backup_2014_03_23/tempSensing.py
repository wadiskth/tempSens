from threading import Thread
import time
#Update the kernel first: sudo vi /etc/apt/sources.list.d/raspi.list
# deb http://archive.raspberrypi.org/debian/ wheezy main untested
# apt get update and upgrade
#Then : 
#sudo modprobe w1-gpio
#sudo modprobe w1-therm
#cd /sys/bus/w1/devices
#ls
#cd 28-xxxx (change this to match what serial number pops up)
#cat w1_slave
#Rpi has power manegment, so :
# open - /etc/kbd/config. and set BLANK_TIME to 0 and POWERDOWN_TIME to 0
class Temp(Thread):
    """
     A class for getting the current temp of a DS18B20
    """

    def __init__(self, fileName):
        Thread.__init__(self)
        self.tempDir = '/sys/bus/w1/devices/'
        self.fileName = fileName
        self.currentTemp = -999
        self.correctionFactor = 1;
        self.enabled = True

    def run(self):
        while True:
            if self.isEnabled():
                try:
                    f = open(self.tempDir + self.fileName + "/w1_slave", 'r')
                except IOError as e:
                    print "Error: File " + self.tempDir + self.fileName + "/w1_slave" + " does not exist.";
                    return;

                lines=f.readlines()
                crcLine=lines[0]
                tempLine=lines[1]
                result_list = tempLine.split("=")

                temp = float(result_list[-1])/1000 # temp in Celcius

                temp = temp + self.correctionFactor # correction factor

    		#if you want to convert to fahrenheit, uncomment this line
                #temp = (9.0/5.0)*temp + 32  
                
                if crcLine.find("NO") > -1:
                    temp = -999

                self.currentTemp = temp
                #print "Current: " + str(self.currentTemp) + " " + str(self.fileName)

            time.sleep(5)

    #returns the current temp for the probe
    def getCurrentTemp(self):
        return self.currentTemp

    #setter to enable this probe
    def setEnabled(self, enabled):
        self.enabled = enabled
    #getter       
    def isEnabled(self):
        return self.enabled

    ####################################################################################################
#from temp import Temp
#import time
#replace tempId with the id of your temperature probe
#wortTemp=Temp(fileName='tempID')
#wortTemp.start()

#the rest of your code is below. 
# The Temp class will be updating on its own thread which will allow you to do 
#  anything you want on the main thread.

#while ( True ): 
#    print str(wortTemp.getCurrentTemp()) 
#    time.sleep(1)
########################################################################################################
#Interesting google spreadsheet logging
#wget https://pypi.python.org/packages/source/g/gspread/gspread-0.0.15.tar.gz#md5=d9fd7c6e3cf29647dfb3b704603b8e38
#tar -zxvf gspread-0.0.15.tar.gz
#cd gspread
#sudo python3 setup.py install

#Then 
#!/usr/bin/python3
 
#import os, glob, time, gspread, sys, datetime
 
#Google account details
#email = 'foo.bar@gmail.com'
#password = 'Foo_Bars_Password'
#spreadsheet = 'Temperature_log' #the name of the spreadsheet already created
 
#attempt to log in to your google account
#try:
#   gc = gspread.login(email,password)
#except:
#    print('fail')
#    sys.exit()
 
#open the spreadsheet
#worksheet = gc.open(spreadsheet).sheet1
 
#  worksheet.append_row(values) #write to the spreadsheet
#  time.sleep(600) #wait 10 minutes
