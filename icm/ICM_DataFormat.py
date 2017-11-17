# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 08:21:46 2017

@author: casari
"""

import numpy as np
import binascii

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
    
    
    
    
def Parse_iData(ds):
    pass
    

def Parse_sData(ds):
    pass

def ParseString(command):
    commands = command.split('@@@')
    crc = CrcCalc()
    for cmd in commands:
        crc.clear()
        mcrc = cmd[0:2]
        mlen = cmd[2:4]
        if(len(cmd)==mlen+4):
            if(crc.add(cmd[2:])==mcrc):
                ParseData(cmd[2:])
                
            
            
            
if __name__ == "__main__":
    crc = CrcCalc()
    
#    data = np.array([1,2,3,4,5])
    data = "1,2,3,4,5"
    
    crc.add(data)
    
    print(hex(crc.crc))
    
    sendstr = '@@@