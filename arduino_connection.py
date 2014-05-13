from threading import Thread
from pyfirmata import Arduino, util
import serial
import time

class ArduinoConnection(Thread):

    def __init__(self):
        Thread.__init__(self)
        
        self.SAMPLING_INTERVAL = 0.100
        self.MEAN_INTERVAL = 5
        self.MEAN_SAMPLES_NUMBER = round(self.MEAN_INTERVAL/self.SAMPLING_INTERVAL)

        PORT = '/dev/ttyACM0'
        self.board = Arduino(PORT)
        it = util.Iterator(self.board)
        it.start()

        self.analog_pin_value_arr = [self.board.get_pin('a:0:i'), self.board.get_pin('a:1:i'), self.board.get_pin('a:2:i'), self.board.get_pin('a:3:i'), self.board.get_pin('a:4:i'), self.board.get_pin('a:5:i')]
        for i in range(len(self.analog_pin_value_arr)):
            self.analog_pin_value_arr[i].enable_reporting()

        self.mean_analog_valuea_arr = [0.0] * 6
        self.mean_analog_valuea_assigned_arr = [0.0] * 6

    def run(self):        
        #s= ''
        sample_number = 0
        
        while True:
            while (sample_number < self.MEAN_SAMPLES_NUMBER):
                #    time.sleep(DELAY)
                self.board.pass_time(self.SAMPLING_INTERVAL)
                for i in range(len(self.mean_analog_valuea_arr)):
                    self.mean_analog_valuea_arr[i] = self.mean_analog_valuea_arr [i] + self.analog_pin_value_arr[i].read()
                sample_number = sample_number + 1

            for i in range(len(self.mean_analog_valuea_arr)):
                self.mean_analog_valuea_arr[i] = self.mean_analog_valuea_arr[i] / self.MEAN_SAMPLES_NUMBER
                #s = s + str(self.mean_analog_valuea_arr[i]) + ' '

            self.mean_analog_valuea_assigned_arr = self.mean_analog_valuea_arr
                
            #print s
            
            #s = ''            
            sample_number = 0
            self.mean_analog_valuea_arr = [0.0] * 6

    def getMeanAnalogArduinoValueArray(self):
        return self.mean_analog_valuea_assigned_arr
