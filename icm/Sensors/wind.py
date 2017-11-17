# -*- coding: utf-8 -*-
""" Wind Sensor Data Parser

This module parses the sData and iData from the PMEL EDD Gill/Ocean Server
wind sensor.


The sData is in the format of:
    'Header Serial Date Time Period<cr>'
    'wind_speed wind_dir heading pitch roll'
    
where:
    Header = Sensor ID
    Serial = Serial Number
    Date = yyyy/mm/dd
    Time[UTC] = hh:mm:ss
    Period = hh:mm:ss
    wind_speed = Raw wind speed * 1000
    wind_dir = Raw wind direction
    heading = Raw heading 
    pitch = Raw pitch * 10
    roll = Raw roll * 10

    

Example(sData):
    'gill_b,2017/06/22,13:49:00,00:02:00<cr>'
     '218,290<cr>'
     '207,310<cr>'
     '232,390'
     
     
The iData is in the format of:
    'Header Date Time windU1 windV1 Speed Gust Heading<cr>'
    
where:
    Header = Sensor ID
    Date = yy/mm/dd
    Time[UTC] = hh:mm:ss
    windU1 = wind U vector (m/s)
    windV1 = wind V vector (m/s)
    Speed = Average wind speed (m/s)
    Gust = Maximum value of the 3-second running average
    Heading = Raw heading 
    
    
Example(iData):
    'gill_b,2017/06/22,13:49:00,00:02:00
     000.0,000.3,0.3,0.4,335.6'
     
    
The response will be a pandas dataframe with the following format:
    timestamp[utc]  wind_speed[m/s]  wind_dir[deg]  heading[deg]  pitch[deg]  roll[deg]
    time[0]         speed[0]         direction[0]   heading[0]    pitch[0]    roll[0]
    ...
    time[n]         speed[n]         directin[n]    heading[n]    pitch[n]    roll[n]



Created on Wed Nov 15 11:04:41 2017


Todo: 
    * iDataParse Function
        * Read Header
        * Read Data

@author: Matt Casari
"""

import pandas as pd
#import numpy as np
import datetime as dt
import io

class DataTime:
    def __init__(self):
        self.period = []
        self.starttime = []
        self.currenttime = []
        

class Data:
    def __init__(self):
        self.serial = []
        self.sensor_id = []
        self.time = DataTime()

    

def sDataParse(msg):
    """ Parse S Data function
    
    Parses a text string (multiple lines) for header and 
    
    Args:
        msg (str): Header and Data fields from sdata response (no @@@,crc or len).  See above for example
    Returns:
        data: Pandas dataframe with format
            timestamp, speed, dir, heading, pitch, roll
    
    
    """
    ## Create an io buffer
    buf = io.StringIO(msg)
    
    #sData = Data()
    sData = _sData_ParseHeader(buf.readline())
    
    ## Create numpy array 
    data = 'timestamp[utc],wind_speed[m/s],wind_dir[deg],heading[deg],pitch[deg],roll[deg]\n'
    
    ## Append the timestamp to the data
    while True:
        nl = buf.readline()
        if nl == '':
            break
        else:
            time = sData.time.currenttime.strftime('%Y/%m/%d %H:%M:%S,')
            sData.time.currenttime += sData.time.period
            
            nl = _sData_DataAdjust(nl)
            data += (time + nl)

    ## Create a pandas Dataframe
    testdata = io.StringIO(data)
    data = pd.read_csv(testdata)
    
    return data


def iDataParse(msg):
    """ Parse I Data function
    
    Parses a text string (multiple lines) for header and 
    
    Args:
        msg (str): Header and Data fields from idata response (no @@@,crc or len).  See above for example
    Returns:
        data: Pandas dataframe with format
            timestamp, u1, v1, speed, gust, heading
    
    
    """
    ## create io buffer
    buf = io.StringIO(msg)
    
    
    data = 'timestamp[utc],u1,v1,wind_speed[m/s],max_gust[m/s],raw_heading[deg]\n'
    
    ## Strip header
    while True:
        nl = buf.readline()
        ## Check for last line
        if(nl ==''):
            break
        
        ## Split the line into values
        vals = nl.split(',')
        
        ## Remove the Sensor ID
        sensor_id = vals.pop(0)

        ## Set the time to the common format
        time = dt.datetime.strptime(vals.pop(0),"%y%m%d %H:%M:%S").strftime('%Y/%m/%d %H:%M:%S')
        
        ## Format the new string
        data += time + ',' + ','.join(str(x) for x in vals)
        
    ## Create a pandas Dataframe
    testdata = io.StringIO(data)
    data = pd.read_csv(testdata)
        
    return data
def _sData_ParseHeader(header):
    """ Parse the header for the sData field
    
    Parses the sData header field
    
    Args:
        header:  Header field for sData field
    Returns:
        sData: Data class
    """
    sData = Data()
    header = header.replace('\n','')
    vals = header.split(',')
     
    sData.sensor_id = vals.pop(0)
    sData.serial = vals.pop(0)
     
    timestr = vals.pop(0) + ' ' + vals.pop(0)
    sData.time.starttime = _Parse_StartTime(timestr)
    sData.time.currenttime = sData.time.starttime
    sData.time.period = _Parse_Period(vals.pop())
     
    return sData

def _sData_DataAdjust(data):
    """ Adjust sData from micro
    Adjusts the micro integers back into their original float format.
    
    Args:
        data (str):  One line of sData
    Returns:
        data (str): Reformatted sData
    
    """
    temp = data.split(',')
    speed = float(temp.pop(0))/1000
    direc = temp.pop(0)
    heading = temp.pop(0)
    pitch = float(temp.pop(0))/10
    roll = float(temp.pop(0))/10
    
    data = str(speed) + ',' + direc + ',' + heading + ',' + str(pitch) + ',' + str(roll) + '\n'
    
    return data
def _Parse_Period(header):
    """ Parse the Header Period for offset time
    
    Parses the header string period field
    
    Args:
        header:  Period field from header
    Returns:
        period: datetime timedelta value for the period
    
    """
    temp = dt.datetime.strptime(header,"%H:%M:%S")
    period = dt.timedelta(hours=temp.hour,minutes=temp.minute,seconds=temp.second)
    
    return period


def _Parse_StartTime(header):
    """ Parse the Header Start Time
    
    Parses the header string time field
    
    Args:
        header:  Date/Time field from header
    Returns:
        period: datetime object value for the start date/time

    """
    temp = dt.datetime.strptime(header,"%Y/%m/%d %H:%M:%S")
    return temp
    
    


if __name__ == '__main__':
    sdata = 'gill_b,wind001,2017/06/22,13:49:00,00:02:00\n218,290,10,11,12\n207,310,13,14,15\n232,390,16,17,18'
    print("\n\nSDATA:")
    print(sDataParse(sdata))
    
    idata = 'gill_b,170622 14:49:00,-0.00,0.0,-0.01,0.1,10\n \
            gill_b,170622 14:51:00,0.10,0.2,0.30,0.4,50'
    print("\n\nIDATA:")
    print(iDataParse(idata))
    
    
