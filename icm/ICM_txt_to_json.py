# -*- coding: utf-8 -*-
""" 
Created on Thu Aug 24 07:43:34 2017


This module takes a text file with the ICM file convention and converts it into
a JSON file which can be imported into the ICM GUI to preconfigure the parameter
tree.


Attributes:
    

@author: casari
"""

import os, re
import json

class ICMMaster():
    """ ICM MASTER Class
    
    This class is designed to hold the ICM MASTER fields loaded from the text
    file.  They will be used in generation of the ICM parameter tree.
    
    Note:
        
    Args:
        None
    Attributes:
        system (str): "MASTER" This field does not change
        serial (str): "SENSORXXX" Temporary field, to be set by user or program
        version (str): "XXX" Temporary field, to be loaded from microcontroller
    """
    def __init__(self):
        """ __init__ Method
        
        The __init__ method creates the initial conditions for the MASTER class
        
        Args:
            None
        
        """
        self.system = "MASTER"
        self.serial = "XXX"
        self.version = "XXX"
    def create_JSON(self):
        """ Creates the JSON output for the MASTER class 
        
        
        """
        pass
    
    
class ICMCom():
    """ ICM COM Port Class
    
    This class is designed hold the ICM COM port class.  The contents of this
    class are used in the generation of the ICM Parameter tree.
    
    Note:

    Args:
        None
    Attributes:
        system (str): This is the COM port number
        name (str): This is the name of the sensor
        prefix (str): A prefix decription
        serial (int): A serial number integer
        baud (int): A baud rate (EIA-232 common)
        warmup (int): warmup time in milli-seconds
        samplestart (str): The HH:MM:SS time to start samples
        sampleinterval (str): The length of time to sample over (HH:MM:SS)
        sampleperiod (str): The period (HH:MM:SS) to sample at
        samplerate (int): The frequency to sample at
        powerswitch (int): Setting to turn power on/off with sample
        command (int): ???
        cmd (str): ???
        header (str): Header to the sensor return string
        format (str): string field types (c=char,f=float)
        column[i] (str): Column headers for i= 0 - n (n =len(format))
    """

    def __init__(self):
        """ Initialization
        
        This __init__ function initializes the COM object and creates empty variables
        for each of the attributes.
        
        Note:
    
        Args:
            None
        
        """
        self.system = []
        self.name = []
        self.prefix = []
        self.serial = []
        self.baud = []
        self.warmup = []
        self.samplestart = []
        self.sampleinterval = []
        self.sampleperiod = []
        self.samplerate = []
        self.powerswitch = []
        self.command = []
        self.cmd = []
        self.header = []
        self.format = []
        self.column = []
        pass
    
    def add(self,text,idx=[]):
        equalIdx = text.find('=')
        try:
            value=text[equalIdx+1:]
        except:
            value=""
        if(text.find('system')>=0):
            self._add_system(value)
        elif(text.find('name')>=0):
            self._add_name(value)
        elif(text.find('prefix')>=0):
            self._add_prefix(value)
        elif(text.find('serial')>=0):
            self._add_serial(value)
        elif(text.find('baud')>=0):
            self._add_baud(value)
        elif(text.find('warmup')>=0):
            self._add_warmup(value)
        elif(text.find('samplestart')>=0):
            self._add_samplestart(value)
        elif(text.find('sampleinterval')>=0):
            self._add_sampleinterval(value)
        elif(text.find('sampleperiod')>=0):
            self._add_sampleperiod(value)
        elif(text.find('samplerate')>=0):
            self._add_samplerate(value)
        elif(text.find('powerswitch')>=0):
            self._add_powerswitch(value)
        elif(text.find('command')>=0):
            self._add_command(value)
        elif(text.find('cmd')>=0):
            if(self.command == 1):
                self._add_cmd(value)
        elif(text.find('header')>=0):
            if(self.command == 1):
                self._add_header(value)
        elif(text.find('format')>=0):
            if(self.command == 1):
                self._add_format(value)
        elif(text.find('column')>=0):
            if(self.command == 1):
                self._add_column(value,idx)
        return
    def _add_system(self,system):
        """ Add System Data
        Adds valid data into the system field
        
        Args:
            system (str): value to add to system attribute
        Returns:
            None
        Raises:
            TypeError: If system value passed is not a string
            ValueError: If system value is too long or too short
            ValueError: If system value is improperly formatted
        
        """
        if(type(system)!=str):
            raise TypeError()
            return
        
        if(len(system)>8):
            raise ValueError()
            return
        
        self.system = system
        
    def _add_name(self,name):
        """ Add Name
        Adds valid data into the name field
        
        Args:
            system (str): value to add to system attribute
        Returns:
            None
        Raises:
            TypeError: If system value passed is not a string
            ValueError: If system value is too long or too short
            ValueError: If system value is improperly formatted
        
        """
        if(type(name)!=str):
            raise TypeError()
            return
        
        if(len(name)>8):
            raise ValueError()
            return
        
        self.name = name
        return
        
    def _add_prefix(self,prefix):
        """ Add Name
        Adds valid data into the prefix field
        
        Args:
            prefix (str): value to add to prefix attribute
        Returns:
            None
        Raises:
            TypeError: If prefix value passed is not a string
            ValueError: If prefix value is too long or too short
            ValueError: If prefix value is improperly formatted
        
        """
        if(type(prefix)!=str):
            raise TypeError()
            return
        
        if(len(prefix)>8):
            raise ValueError()
            return
        
        self.prefix = prefix
        return
    
    def _add_serial(self,serial):
        """ Add Name
        Adds valid data into the serial field
        
        Args:
            serial (int): value to add to serial attribute
        Returns:
            None
        Raises:
            TypeError: If serial value passed is not an int
            ValueError: If serial value is < 0 or > 255
        
        """
        try:
            serial = int(serial)
        except:
            raise TypeError(serial)
#        if(type(serial)!=str):
#            raise TypeError()
#            return
        
        if((serial < 0) or (serial > 255)):
            raise ValueError()
            return
        
        self.serial = serial
        return
    
    def _add_baud(self,baud):
        """ Add Name
        Adds valid data into the baud field
        
        Args:
            baud (int): value to add to baud attribute
        Returns:
            None
        Raises:
            TypeError: If baud value passed is not an int
            ValueError: If baud value is < 0 or > 255
        
        """
        try:
            baud = int(baud)
        except:
            raise TypeError
#        if(type(baud)!=int):
#            raise TypeError()
#            return
        
        if( baud == 1200 or
            baud == 2400 or
            baud == 4800 or
            baud == 9600 or
            baud == 19200 or
            baud == 28800 or
            baud == 38400 or
            baud == 57600 or
            baud == 115200):
            
            self.baud = baud
        else:
            raise ValueError()
            return
        
        return
    
    
    def _add_warmup(self,warmup):
        """ Add Name
        Adds valid data into the warmup field
        
        Args:
            warmup (int): value to add to system attribute
        Returns:
            None
        Raises:
            TypeError: If warmup value passed is not an int
            ValueError: If warmup value is < 0 or > 255
        
        """
        try:
            warmup = int(warmup)
        except:
            raise TypeError("Invalid Warmup Value")
 
        
        if((warmup < 0) or (warmup > 60000)):
            raise ValueError()
            return
        
        self.warmup = warmup
        return
        
    def _add_samplestart(self,samplestart):
        """ Add Name
        Adds valid data into the samplestart field
        
        Args:
            samplestart (str): value to add to samplestart attribute
        Returns:
            None
        Raises:
            TypeError: If samplestart value passed is not an str
            ValueError: If the samplestart time values are incorrect (24 hour clock)55
        
        """
        if(type(samplestart)!=str):
            raise TypeError()
            return
        
        if((samplestart.count(':') == 2) and (len(samplestart) == 8) and
           (int(samplestart[0:2]) >= 0) and (int(samplestart[0:2]) < 24) and
           (int(samplestart[3:5]) >= 0) and (int(samplestart[3:5]) < 60) and
           (int(samplestart[6:8]) >= 0) and (int(samplestart[6:8]) < 60)):
           pass
        else:
            raise ValueError("Invalid samplestart value")
            return
        
        self.samplestart = samplestart
        return
    
    def _add_sampleinterval(self,sampleinterval):
        """ Add Name
        Adds valid data into the sampleinterval field
        
        Args:
            sampleinterval (str): value to add to sampleinterval attribute
        Returns:
            None
        Raises:
            TypeError: If sampleinterval value passed is not a str
            ValueError: If the sampleinterval time values are incorrect (24 hour clock)
        
        """
        if(type(sampleinterval)!=str):
            raise TypeError()
            return
        
        if((sampleinterval.count(':') == 2) and (len(sampleinterval) == 8) and
           (int(sampleinterval[0:2]) >= 0) and (int(sampleinterval[0:2]) < 24) and
           (int(sampleinterval[3:5]) >= 0) and (int(sampleinterval[3:5]) < 60) and
           (int(sampleinterval[6:8])>= 0) and (int(sampleinterval[6:8]) < 60)):
           pass
        else:
            raise ValueError()
            return
        
        self.sampleinterval = sampleinterval
        return

    def _add_sampleperiod(self,sampleperiod):
        """ Add Name
        Adds valid data into the sampleperiod field
        
        Args:
            sampleperiod (str): value to add to sampleperiod attribute
        Returns:
            None
        Raises:
            TypeError: If sampleperiod value passed is not a str
            ValueError: If the sampleperiod time values are incorrect (24 hour clock)
        
        """
        if(type(sampleperiod)!=str):
            raise TypeError()
            return
        
        if((sampleperiod.count(':') == 2) and (len(sampleperiod) == 8) and
           (int(sampleperiod[0:2]) >= 0) and (int(sampleperiod[0:2]) < 24) and
           (int(sampleperiod[3:5]) >= 0) and (int(sampleperiod[3:5]) < 60) and
           (int(sampleperiod[6:8]) >= 0) and (int(sampleperiod[6:8]) < 60)):
           pass
        else:
            raise ValueError()
            return
        
        self.sampleperiod = sampleperiod
        return    
    
    def _add_samplerate(self,samplerate):
        """ Add Name
        Adds valid data into the samplerate field
        
        Args:
            samplerate (int): value to add to system attribute
        Returns:
            None
        Raises:
            TypeError: If samplerate value passed is not an int
            ValueError: If samplerate value is < 0 or > 100
        
        """
        try:
            samplerate = int(samplerate)
        except:
            raise TypeError("Invalid samplerate value")
        
        if((samplerate < 0) or (samplerate > 100)):
            raise ValueError()
            return
        
        self.samplerate = samplerate
        return

    def _add_powerswitch(self,powerswitch):
        """ Add Name
        Adds valid data into the powerswitch field
        
        Args:
            powerswitch (int): value to add to powerswitch attribute
        Returns:
            None
        Raises:
            TypeError: If powerswitch value passed is not an int
            ValueError: If powerswitch value is < 0 or > 1
        
        """
        try:
            powerswitch = int(powerswitch)
        except:
            raise TypeError("Invalid powerswitch value")

        
        if((powerswitch < 0) or (powerswitch > 1)):
            raise ValueError()
            return
        
        self.powerswitch = powerswitch
        return
    
    def _add_command(self,command):
        """ Add Name
        Adds valid data into the command field
        
        Args:
            command (str): value to add to command attribute
        Returns:
            None
        Raises:
            TypeError: If command value passed is not a string
            ValueError: If command value is too long or too short
            ValueError: If command value is improperly formatted
        
        """
        try:
            command = int(command)
        except:
            raise TypeError("Invalid command value")
             
        if((command < 0) or (command > 1)):
            raise ValueError("Invalid command value")
        else:
            self.command = command
        return
    
    def _add_cmd(self,cmd):
        """ Add Name
        Adds valid data into the cmd field
        
        Args:
            cmd (str): value to add to cmd attribute
        Returns:
            None
        Raises:
            TypeError: If cmd value passed is not a string
            ValueError: If cmd value is too long or too short
            ValueError: If cmd value is improperly formatted
        
        """
        if(type(cmd)!=str):
            raise TypeError()        
        elif(len(cmd)>8):
            raise ValueError()
        else:
            self.cmd = cmd
        return

    def _add_header(self,header):
        """ Add Name
        Adds valid data into the header field
        
        Args:
            header (str): value to add to header attribute
        Returns:
            None
        Raises:
            TypeError: If header value passed is not a string
            ValueError: If header value is too long or too short
            ValueError: If header value is improperly formatted
        
        """
        if(type(header)!=str):
            raise TypeError()        
        elif(len(header)>8):
            raise ValueError()
        else:
            self.header = header
        return

    def _add_format(self,frmt):
        """ Add Name
        Adds valid data into the frmt field
        
        Args:
            header (str): value to add to frmt attribute
        Returns:
            None
        Raises:
            TypeError: If frmt value passed is not a string
            ValueError: If frmt value is too long or too short
            ValueError: If frmt value is improperly formatted
        
        """
        if(type(frmt)!=str):
            raise TypeError()        
        elif(len(frmt)>8):
            raise ValueError()
        else:
            self.format = frmt
            self.columnLength = len(frmt)
            self.column =[]
            for i in range(0,self.columnLength):
                self.column.append([])
        return
    
    def _add_column(self,column,columnNumber):
        """ Add Name
        Adds valid data into the column field
        
        Args:
            column (str): value to add to column attribute
        Returns:
            None
        Raises:
            TypeError: If column value passed is not a string
            ValueError: If column value is too long or too short
            ValueError: If column value is improperly formatted
        
        """
        if((type(column)!=str) or (type(columnNumber) != int)):
            raise TypeError()        
        elif(columnNumber>self.columnLength):
            raise ValueError()
        else:
            self.column[columnNumber] = column
        return
class ICMParam():
    """ Class to hold the loaded ICM Parameters
    
    This class is designed to hold all of the possible ICM parameters loaded 
    from the text file.  
    
    Note:
    
    Args:
        None
    
    Attributes:
        master (ICMMaster): Master Class
        COM[i] (ICMCom): COM classes from 1 to n (n=length(system))
    """
    def __init__(self,numCOM):
        """ Initialize the ICMParam Object
        
        The __init__ function intializes the ICMParam Object based on the number
        of COM ports defined in the text file.
        
        Note:
            
        Args:
            numCOM (int):  Number of COM objects required for sensor
        """
        self.master = ICMMaster()
        self.com = []
        self._numCom = numCOM
        for i in range(0,numCOM):
            self.com.append(ICMCom())
            
    def parse_text(self,text):
        t = text.split('\n')
        for item in t:
            if(item.find('MASTER')>=0):
                currentSystem = 'MASTER'
                
            elif(item.find('COM')>=0):
                currentSystem = 'COM'
                comIdx= int(item[item.find('COM')+3:])
                columnNum = 0
                self.com[comIdx-1].add(item)
            else:
                if(currentSystem == 'MASTER'):
                    pass
                elif(currentSystem == 'COM'):
                    if(comIdx > self._numCom):
                        raise ValueError("Illegal COM value")
                    else:
                        if(item.find('column')>=0):
                            self.com[comIdx-1].add(item,columnNum)
                            columnNum += 1
                        else:
                            self.com[comIdx-1].add(item)
        return
    
    def generate_JSON(self):
        """ ICM JSON data generation
        
        This function takes a populated ICMParam class and generates the JSON
        data needed to create the parameter tree in the ICM GUI.
        
        Note:
            
        Args:
            none
        Returns:
            json (JSON data): The generated json text to save to a file
        Raises:
            ValueError: Invalid valueS
        """   
        ## Create the dict used to populate the JSON data
        
        data = dict()
        master = [[],[],[]]

        
        ## Add the Master fields
        master[0] = {'name': 'System','type':'str','value':'MASTER'}
        master[1] = {'name':'PMEL Serial Number','type':'str','value':'XXXXXXXXXX'}
        master[2] = {'name':'Firmware Version','type':'str','value':'XXXXXXXXXX'}
        
        data['MASTER'] = master
        
        ## Iterate through COMs and add fields to data
        for i in range(0,self._numCom):
            c = self._add_com_param_to_object(i)
            data['COM{}'.format(i+1)] = c
                
        return data


    def _add_com_param_to_object(self,comNum):
    
        com = []
        
        com.append({'name':'Name','type':'str','value':self.com[comNum].name})
        com.append({'name':'Prefix','type':'str','value':self.com[comNum].prefix})
        com.append({'name':'Serial Port','type':'str','value':self.com[comNum].serial})
        com.append({'name':'Baud Rate','type':'list',
                    'values':['1200','2400','4800','9600','19200','28800','57600','115200'],
                    'value':self.com[comNum].baud})
        com.append({'name':'Warmup Time','type':'int','value':self.com[comNum].warmup})
        com.append({'name':'Sample Start Time','type':'str','value':self.com[comNum].samplestart})
        com.append({'name':'Sample Interval','type':'str','value':self.com[comNum].sampleinterval})
        com.append({'name':'Sample Period','type':'str','value':self.com[comNum].sampleperiod})
        com.append({'name':'Sample Rate','type':'int','value':self.com[comNum].samplerate})
        com.append({'name':'Power Switch','type':'int','value':self.com[comNum].powerswitch})
        com.append({'name':'Command','type':'str','value':self.com[comNum].command})
        if(self.com[comNum].command == '1'):
            com.append({'name':'cmd','type':'str','value':self.com[comNum].cmd})
            com.append({'name':'header','type':'str','value':self.com[comNum].header})
            com.append({'name':'format','type':'str','value':self.com[comNum].format})
            for i in range(0,len(self.com[comNum].column)):
                com.append({'name':'column[{}]'.format(i),'type':'str','value':''})
        com.append({'name':'=end'})
    
        return com
    
    
    
    
def icm_txt_to_json(filepath,overwrite=True):
    """ Converts an ICM text file to the JSON format
    This file takes an ICM text file and converts it to the JSON format that is
    used to load the parameter tree in the ICM GUI.  The JSON format is saved in
    a JSON folder within the sensor folder.
    
    The J
    
    Args:
        filepath (str): The path to the text file to be converted
    
    Raises:
        IOError: If the path is invalid
        ValueError: If the file already exists and overwrite == False
        AttributeError: If the JSON file 
    
    """
    path = os.path.join('.','sensors')
    jpath = os.path.join(path,'json')
    filename = filepath[filepath.rfind('\\')+1:filepath.rfind('.')]
    
    ## Open the file
    try:
        f = open(filepath,mode='r')
        t = f.read()
    except:
        raise IOError
        return
      
    ## Parse the ICM Text Data
    param = _parse_icm_text_file(t)
    
    ## Does a JSON file exist?
    jfilename = filename + ".json"
    jfilepath = os.path.join(jpath,jfilename)
    
    if(overwrite==False):
        if(os.path.exists(jfilepath)==True):
            raise IOError('JSON File already exists')

    
    ## Generate the JSON data
    jsonData = param.generate_JSON()
    
    cwd = os.getcwd()
    os.chdir('..')
    f = open(jfilepath,'w')
    #with open(jfilepath,'w') as outfile:
    json.dump(jsonData,f,indent=4)
    os.chdir(cwd)
    

    
    return param

def _parse_icm_text_file(filetext):
    """ Parses the contents of ICM text file
    
    This file takes the contents of the ICM text file, creates an ICMParam object
    based on the number of COM ports uses, and populates the ICMParam object 
    with the data parsed from the text.
    
    Args:
        filetext (str): The file contents of the ICM text file.
    
    Returns:
        param (ICMParam): The ICMParam Object created
    Raises:
        ValueError: If the value of any parameter is not valid
    
    """
    ## Check there is a master section of the file
    numMASTER = filetext.count('MASTER')
    if(numMASTER != 1):
        raise ValueError('Invalid Number (MASTER)')
        return

    ## Test the number of COM is between 1 - 3
    numCOM = filetext.count('COM')
    if(numCOM == 0 or numCOM > 3):
        raise ValueError
        return

    ## Create the ICMParam Object
    param = ICMParam(numCOM)
    param.parse_text(filetext)
    return param
#    for i in range(0,numCOM):
#        text = param.com[i].__dict__
#        print(text)
        #print(param.com[i].__dict__)
if __name__ == "__main__":              
    
    path = 'C:\\Users\\Casari\\version-control\\PMEL\\EDD-ICMGUI\\icm\\Test.txt'
    temp = icm_txt_to_json(path)
    for i in range(0,temp._numCom):
        d = temp.com[i].__dict__
        for k,v in d.items():
            if(v==[]):
                pass
            elif(k=='column'):
                for item in v:
                    print(k,'=',item,sep="")
            else:
                    print(k,'=',v,sep="")
        print('=end')