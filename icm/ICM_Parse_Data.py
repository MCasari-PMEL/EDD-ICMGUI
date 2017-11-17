# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 09:05:01 2017

@author: casari
"""
import pandas as pd
import numpy as np
import Sensors.wind as wind
# import imm
# import 



class CrcCalc():
    def __init__(self):
        self.crc = 0
    def add(self,data):
        accum = np.uint32(0)
        for i in data:
            ch = np.uint32(ord(i))
            accum = self._accum_crc(accum,ch)
        
        accum = self._accum_crc(accum,0)
        accum = self._accum_crc(accum,0)
        
        self.crc = (accum >> 8)
        
        return self.crc
    
    def clear(self):
        self.crc = 0
    
    def _accum_crc(self,accum,ch):
        i = np.int16(0)
        acmul = np.uint32(0)
        
        temp = np.uint32(ch & 0xFF)
        acmul = np.uint32(accum | temp)
        
        for i in range(0,8):
            acmul = acmul << 1
            if(acmul & 0x1000000):
                acmul = acmul ^ 0x102100
        
        return acmul
    


''' This class interprets and stores data in a numpy array so that it is 
generically useable in the ICM GUI, unlike the common ICM data format.

The data format of the subsensor must be returned as an array with the first
column being the timestamp

'''
class ICMData:
    def __init__(self):
        self.sData = []
        self.iData = []
        self.crc = CrcCalc()
        
#        self.sData = pd.DataFrame([])
    
    
    def Clear_Data(self):
        self.sData = []
        self.iData = []
    def Parse_Data(self,data,cmd,sensor):
        ## Strip the wrapped data (crc, len)
        data = data[data.find('@@@')+3:]
#        crc = data[0:2]
        crc = int(data[0]) * 8 + int(data[1])
        dlen = int(data[2])*8 + int(data[3])
        data = data[5:]
        
        
        ## Check the CRC
        self.crc.clear()
        
        calccrc = self.crc.add(data)
        try:
            calccrc = self.crc.add(data)
#            assert(calccrc==crc)
        except:
            print("Invalid CRC")
            raise(ValueError)
        
        ## Check the sub
        if(cmd == 'sData'):
            if(sensor=='wind'):
                temp = wind.sDataParse(data)
                pass
            if(sensor=='rain'):
                #temp = rain.sDataParse(data)
                pass
            if(sensor=='load'):
                #temp = load.sDataParse(data)
                pass
        
            if(len(self.sData)==0):
                self.sData = temp
            else:
                self.sData = self.sData.append(temp,ignore_index=True)

#                self.sData = pd.concat(self.sData,temp)
        if(cmd == 'iData'):   
            if(sensor=='wind'):
                temp = wind.iDataParse(data)
                pass
            if(sensor=='rain'):
                #temp = rain.sDataParse(data)
                pass
            if(sensor=='load'):
                #temp = load.sDataParse(data)
                pass

            if(len(self.iData)==0):
                self.iData = temp
            else:
                self.iData = self.iData.append(temp,ignore_index=True)

if __name__ == '__main__':
    sdata1 = '@@@3294,gill_b,wind001,2017/06/22,13:49:00,00:02:00\n218,290,10,11,12\n207,310,13,14,15\n232,390,16,17,18'
    sdata2 = '@@@3276,gill_b,wind001,2017/06/22,14:49:00,00:02:00\n128,326,10,11,12\n207,310,13,14,15\n232,390,16,17,18'
    idata1 = '@@@3294,gill_b,170622 14:49:00,-0.00,0.0,-0.01,0.1,10\n \
             gill_b,170622 14:51:00,0.10,0.2,0.30,0.4,50'
    idata2 = '@@@3294,gill_b,170622 13:49:00,-0.20,0.2,-0.21,0.1,12\n \
             gill_b,170622 15:51:00,1.10,1.2,1.30,1.4,51'
    data = ICMData()
    
    data.Parse_Data(sdata1,'sData','wind')
    data.Parse_Data(sdata2,'sData','wind')
    data.Parse_Data(idata1,'iData','wind')    
    data.Parse_Data(idata2,'iData','wind')    

    print(data.sData)
    print(data.iData)