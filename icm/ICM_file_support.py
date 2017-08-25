# -*- coding: utf-8 -*-
"""
This script generates the ICM control file from the provided parameters

"""

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from ICM_parameters import *

#app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType

import os
import sys


""" Parse the ICM Parameters that are read

Args:
  Line from text file
Returns:
  There are no returns for this function

Raises:
  Value error: Invalid Parameters
"""
def parseICMFile(icm,parameters):
    system = "MASTER"
    serial = []
    version = []
    prefix = []
    baud = []
    warmup = []
    samplestart = []
    sampleinterval = []
    sampleperiod = []
    samplerate = []
    powerswitch = []
    command = []
    cmd = []
    header = []
    fformat = []
    column = []
    columnNum = 0
    print(parameters)
    
    try:
        for line in icm:
            #print(line)
            value = line[line.find("=")+1:]
            if(line.find("system=")==0):
                system = line[line.find("=")+1:]
            elif(line.find("serial=")==0):
                #print(system)
                if(system == "MASTER"):
                    print("In Here")
                    parameters[system][1]['PMEL Serial Number'] = value
                else:
                    parameters[system][1]['Serial Port'] = line[line.find("=")+1:]
            elif(line.find("version=")==0):
                parameters[system][1]['Firmware Version'] = line[line.find("=")+1:]
            elif(line.find("name=")==0):
                parameters[system][1]['Name'] = line[line.find("=")+1:]
            elif(line.find("prefix=")==0):
                parameters[system][1]['Prefix'] = line[line.find("=")+1:]
            elif(line.find("baud=")==0):
                parameters[system][1]['Baud Rate'] = line[line.find("=")+1:]
            elif(line.find("warmup=")==0):
                parameters[system][1]['Warmup Time'] = line[line.find("=")+1:]
            elif(line.find("samplestart=")==0):
                parameters[system][1]['Sample Start Time'] = line[line.find("=")]
            elif(line.find("sampleinterval=")==0):
                parameters[system][1]['Sample Interval'] = line[line.find("=")]
            elif(line.find("samplerate=")==0):
                parameters[system][1]['Sample Rate'] = line[line.find("=")]
            elif(line.find("powerswitch=")==0):
                parameters[system][1]['Power Switch'] = line[line.find("=")]
            elif(line.find("command=")==0):
                parameters[system][1]['Command'] = line[line.find("=")]
            elif(line.find("cmd=")==0):
                parameters[system][1]['cmd'] = line[line.find("=")]
            elif(line.find("header=")==0):
                parameters[system][1]['header'] = line[line.find("=")]
            elif(line.find("format")==0):
                parameters[system][1]['format'] = line[line.find("=")]
            elif(line.find("column=")==0):
                parameters[system][1]['column['+str(columnNum) + ']'] = line[line.find("=")]
                columnNum += 1
    except:
        print("Invalid File")

    return parameters




def parseConfigFile(parameters,file):
    pass



""" Generate ICM File
Takes the parameters for the ICM file and creates a text file.

Args:
  Structured dictionary of ICM parameters

Returns:
  There are no returns for this function

Raises:
    Value Error: Invalid Parameters

"""
def interpretICMFile(parameters,file):
    
    try:
        with open(file,'r') as f:
            stocks = f.read().splitlines()
            parameters = parseICMFile(stocks,parameters)

    except:
        pass
    return parameters
    
    
def deleteICMFile(file):
    try:
        os.remove(file)
        
    except:
        pass


def populateICMParametersFromJSON(file):
    


def parseICMParameters(parameters):
    ## Create a list of the main parameters (Master, COM1, COM2, etc.)
    #print("\r\n\r\n\r\n")
#    print(type(parameters))
    items = list(parameters)
#    print(type(items))
    #
    content = []
    
    for item in items:
#        print("\r\n\r\n****\r\n")
#        print(item)
        
        if item == 'MASTER':
            #print("In Master")
            content += 'system=MASTER\n'
            #print(content)
            content += 'serial={}\n'.format(parameters[item][1]['PMEL Serial Number'][0])
            #print(content)
            content += 'version={}\n'.format(parameters[item][1]['Firmware Version'][0])
            
            
        elif item.find("COM")!= -1:
            content += 'system={}\n'.format(item)
            content += 'name={}\n'.format(parameters[item][1]['Name'][0])
            content += 'prefix={}\n'.format(parameters[item][1]['Prefix'][0])
            content += 'serial={}\n'.format(parameters[item][1]['Serial Port'][0])
            content += 'baud={}\n'.format(parameters[item][1]['Baud Rate'][0])
            content += 'warmup={}\n'.format(parameters[item][1]['Warmup Time'][0])
            content += 'samplestart={}\n'.format(parameters[item][1]['Sample Start Time'][0])
            content += 'sampleinterval={}\n'.format(parameters[item][1]['Sample Interval'][0])
            content += 'sampleperiod={}\n'.format(parameters[item][1]['Sample Period'][0])
            content += 'samplerate={}\n'.format(parameters[item][1]['Sample Rate'][0])
            content += 'powerswitch={}\n'.format(parameters[item][1]['Power Switch'][0])
            content += 'command={}\n'.format(parameters[item][1]['Command'][0])
            content += 'cmd={}\n'.format(parameters[item][1]['cmd'][0])
            content += 'header={}\n'.format(parameters[item][1]['header'][0])
            content += 'format={}\n'.format(parameters[item][1]['format'][0])
            for i in range(0,len(parameters[item][1]['format'][0])):
                col = 'column[{}]'.format(i)
                #print(col)
                if(parameters[item][1][col][0] != ''):
                    content += 'column={}\n'.format(parameters[item][1][col][0])
            
            content += '=end\n'
            
        #print(content)
    return content




""" Generate ICM File
Takes the parameters for the ICM file and creates a text file.

Args:
  Structured dictionary of ICM parameters

Returns:
  There are no returns for this function

Raises:
    Value Error: Invalid Parameters

"""
def generateICMFile(parameters,file):
    filecontent = parseICMParameters(parameters)
    

    try:
        with open(file,'w') as f:
            for t in filecontent:
                f.write(t)
    except:
        pass
    return filecontent
    
    
    
    

if __name__ == "__main__":              
    
    p0 = Parameter.create(name='Master',type='group',children=master_params_1_0_0)
    p1 = Parameter.create(name='COM1',type='group',children=com_params_1_0_0)
    p2 = Parameter.create(name='COM2',type='group',children=com_params_1_0_0)
    p3 = Parameter.create(name='COM3',type='group',children=com_params_1_0_0)
        
    p0.addChild(p1)
    p0.addChild(p2)
    p0.addChild(p3)
    
    v = p0.getValues()
    #print(parseParameters(v))
    
    path = os.getcwd()
    file = os.path.join(path,'Test.txt')
    generateICMFile(v,file)
