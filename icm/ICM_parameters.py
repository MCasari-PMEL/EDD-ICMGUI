# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 09:43:17 2017

@author: casari
"""

master_params_1_0_0 = [
    {'name': 'MASTER','type':'group','children': [
                                            
#        {'name':'System','type':'list','values':['Master','COM1','COM2','COM3'],'value':0},
        {'name': 'System','type':'str','value':'MASTER'},
        {'name':'PMEL Serial Number','type':'str','value':'XXXXXXXXXX'},
        {'name':'Firmware Version','type':'str','value':'XXXXXXXXXX'}
        ]} ]


com_params_1_0_0 = [   {'name':'Name','type':'str','value':'NAME'},
                {'name':'Prefix','type':'str','value':'PREFIX'},
                {'name':'Serial Port','type':'str','value':'XXXX'},
                {'name':'Baud Rate','type':'list','values':['1200','2400','4800','9600','19200','28800','57600','115200'],'value':'9600'},
                {'name':'Warmup Time','type':'int','value':12000},
                {'name':'Sample Start Time','type':'str','value':'00:00:00'},
                {'name':'Sample Interval','type':'str','value':'00:00:00'},
                {'name':'Sample Period','type':'str','value':'00:00:00'},
                {'name':'Sample Rate','type':'int','value':1},
                {'name':'Power Switch','type':'int','value':1},
                {'name':'Command','type':'str','value':'0'},
                {'name':'cmd','type':'str','value':""},
                {'name':'header','type':'str','value':'$'},
                {'name':'format','type':'str','value':''},
                {'name':'column[0]','type':'str','value':''},
                {'name':'column[1]','type':'str','value':''},
                {'name':'column[2]','type':'str','value':''},
                {'name':'column[3]','type':'str','value':''},
                {'name':'column[4]','type':'str','value':''},
                {'name':'column[5]','type':'str','value':''},
                {'name':'column[6]','type':'str','value':''},
                {'name':'column[7]','type':'str','value':''},
                {'name':'=end'} ]

com_params_0_0_1 = [   {'name':'Name','type':'str','value':'NAME'},
                {'name':'Prefix','type':'str','value':'PREFIX'},
                {'name':'Serial Port','type':'str','value':'XXXX'},
                {'name':'Baud Rate','type':'list','values':['1200','2400','4800','9600','19200','28800','57600','115200'],'value':'9600'},
                {'name':'Warmup Time','type':'int','value':12000},
                {'name':'Sample Start Time','type':'str','value':'00:00:00'},
                {'name':'Sample Interval','type':'str','value':'00:00:00'},
                {'name':'Sample Period','type':'str','value':'00:00:00'},
                {'name':'Sample Rate','type':'int','value':1},
                {'name':'Power Switch','type':'int','value':1},
                {'name':'Command','type':'str','value':'0'},
                {'name':'cmd','type':'str','value':""},
                {'name':'header','type':'str','value':'$'},
                {'name':'format','type':'str','value':''},
                {'name':'=end'} ]