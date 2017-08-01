# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:23:21 2017

@author: casari
"""
import sys, os, time, glob, serial

class SerialPort:
    def __init__(self):
        
        self.serial = serial.Serial()
        
        self.serial.baudrate = 9600
        
        self.portnames = []
        self.timeout = 0.1
        
        
        ## Find all ports
        self.find_available_ports()
        
    def setPort(self,port):
        self.serial.port = port
        
    def setBaud(self,baud):
        self.serial.baudrate = baud
    
    def setParity(self,parity):
        self.serial.parity = parity
    
    def setBytesize(self,bytesize):
        self.serial.bytesize = bytesize
        
    def setStopbits(self,stopbits):
        self.serial.stopbits = stopbits
    
    def setTimeout(self,timeout):
        self.serial.timeout = timeout
        
    def start(self):
        
        self.serial.open()
        if self.serial.is_open == True:
            print("Connected!")
        else:
            print("Unable to Connect")

    def stop(self):
        self.serial.close()

    def read(self):
        self.buffer = self.serial.read_all()
        
    def write(self,value):
        self.serial.write(value)
        
    def find_available_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i+1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported Platform')

        del(self.portnames)
        self.portnames = []

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self.portnames.append(port)
            except (OSError,serial.SerialException):
                pass
    
            
            

        
        
if __name__ == "__main__":      
    
    Port = SerialPort()