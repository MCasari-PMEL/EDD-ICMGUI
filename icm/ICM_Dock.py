# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 14:18:56 2017

@author: casari
"""


import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import qApp
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.Point import Point
from pyqtgraph.dockarea import *
import pyqtgraph.console

import numpy as np
import os
import sys
import serial
import json 
from pprint import pprint

from ui_parameter import *
from ui_serial import *
from ui_commands import *
from ui_plot import *
from ICM_file_support import *


class Communicate(QObject):
    closeApp = pyqtSignal()

class MainWindow(QtGui.QMainWindow):

    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self._version_string = "1.0.1"
        ## Create a communication event to close the window
        self.c = Communicate()
        self.c.closeApp.connect(self.close)
        
        ## Read the config file
        self.read_config()

        ## Add the menu bar
        self.add_menubar()

        ## Create docks, place them into the window one at a time.
        ## Note that size arguments are only a suggestion; docks will still have to
        ## fill the entire dock area and obey the limits of their internal widgets.
        self.area = DockArea()
        
        self.headerDock = Dock("Description",size=(200,5))
        self.plotDock = Dock("Plot",size=(900,300))
        self.sParamDock = Dock("Program Parameters",size=(200,200))
        self.dParamDock = Dock("On-Device Parameters",size=(200,200))
        self.fileDock = Dock("Create File",size=(60,25))
        self.serialDock = Dock("Serial Port",size=(60,25))
        self.meatballDock = Dock("PMEL Logo",size=(60,25))

        self.area.addDock(self.headerDock,'top')
        self.area.addDock(self.plotDock,'bottom',self.headerDock)
        self.area.addDock(self.fileDock,'left',self.plotDock)
        self.area.addDock(self.serialDock,'bottom',self.fileDock)
        self.area.addDock(self.meatballDock,'bottom',self.serialDock)
        
        self.area.addDock(self.dParamDock,'right',self.plotDock)
        self.area.addDock(self.sParamDock,'above',self.dParamDock)
        
        
        
        ## Add widgets into each dock
        ## GUI Description
        self.header = pg.LayoutWidget()
        self.header.setAutoFillBackground(True)
        palette = self.header.palette()
        label = QtGui.QLabel(""" ICM Graphic User Interface """)
        font = QtGui.QFont( "Helvetica", 18)
        font.setBold(True)
        label.setFont(font)
        label.setStyleSheet("color: black")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.header.addWidget(label, row=0, col=0)
        self.headerDock.addWidget(self.header)
        self.headerDock.hideTitleBar()
        
        ## Add Plot Widget
#        self.plot = Graph(8,2)
        self.plot = Graph(2,4)
        self.plotDock.addWidget(self.plot)
        
        
        ## Add Device and System Parameters Widget
        self.dParams = ICMParams()
        self.sParams = ICMParams()
        self.dParams.disable_checkboxes(True)        
        self.dParams.disable_parameters(True)
        
        self.sParamDock.addWidget(self.sParams)
        self.dParamDock.addWidget(self.dParams)
        #paramTabs = QTabWidget()
        #paramTabs.addTab(self.sParams,'Load Parameters')
        #paramTabs.addTab(self.dParams,'Device Parameters')
        #self.paramDock.addWidget(paramTabs)
        
        
        ## Add Serial Port Widget
        self.serial = SerialPort()
        self.serialDock.addWidget(self.serial)
        
        ## Add Create File
        self.file_ = CommandWidget()
        self.fileDock.addWidget(self.file_)
        
        ## Add Meatball
        self.meatball = pg.LayoutWidget()
        pic = QtGui.QLabel()
        pixmap = QtGui.QPixmap("PMEL.png")
        pic.setPixmap(pixmap)
        pic.setScaledContents(True)
        pic.setMaximumSize(150,150)
        self.meatball.addWidget(pic, row=0, col=0)
        self.meatballDock.addWidget(self.meatball)
        self.meatballDock.hideTitleBar()
        
        ## Connect the button signals
        self.connect_buttons()
        
        ## Set the number of vars and sensor type
        self.icm_type = "None"
        self.num_sVars = 0
        self.num_iVars = 0
        
        
        #self.setFixedSize(1200,700)
        
        self.setCentralWidget(self.area)
        
    def read_config(self):
        ## Load list of configurations
        path = os.getcwd()
        os.chdir('..')
        filename = os.path.join(os.getcwd(),'config.json')
        os.chdir(path)


        with open(filename) as json_data:
            self.config = json.load(json_data)
            #pprint(d)
            
        
            
            
    def add_menubar(self):
        ## Add File menu Actions
        exitAct = QAction('&Quit',self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)
        
        ## Create the menubar
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        icmMenu = menubar.addMenu('&ICM Config')
        helpMenu = menubar.addMenu('&Help')
        
        

                                 
        fileMenu.addAction(exitAct)
        
        
        
        ## Populate the ICM menu
        for item in self.config['ICMConfigs']:
            icmAct = QAction(item['name'],self)
            icmAct.triggered.connect( lambda checked,name=item['file']:self._read_param_file(name))
            icmMenu.addAction(icmAct)

            
        
        ## Add to Help menu
        helpMenu.addAction('About ICM Interface')
        helpMenu.triggered.connect(self.help)
        
    def _read_param_file(self,index):
        try:
            self.sParams.UpdateParams(index)
            ## Set the graph up for the right number of variables
            if(index == "Rain Gauge (RAIN)"):
                self.icm_type = "Rain"
                self.num_sVars = 8
                self.num_iVars = 4
            if(index == "Wind Sensor (WIND)"):
                self.icm_type = "Wind"
                self.sParam.num_sVars = 6
                self.sParam.num_iVars = 4
                
            self.plot.reset_num_vars(self.num_sVars,self.num_iVars)
        except IOError:
            print("File Not Found")
            self._errorMsg('File')
        QApplication.processEvents()
        
        #icmMenu.addMenu('Test')
    def connect_buttons(self):
        """ Button Signal Connects
        
        Connects button signals to functions
        
        Args:
            None
        Returns:
            None
        
        """
        self.file_.port_btn.clicked.connect(self._save_file)
        self.file_.clear_btn.clicked.connect(self._clear_data)
        self.file_.retr_btn.clicked.connect(self._retreive_file)
        self.file_.sdata_btn.clicked.connect(self._sdata)
        self.file_.idata_btn.clicked.connect(self._idata)
        
    def _sdata(self):
        """ Retreive SDATA button function
        
        Commands ICM for SDATA, parses response and displays on graph
        
        Args:
            None
        Returns:
            None
        """
        print('sdata')
        ## ***DEBUG ONLY***
        update('sdata')
        ## Send SDATA Command to ICM
        try:
            assert(self.serial.serial.is_open == True)
            self.serial.serial.write(b"SDATA\n")
        except:
            self._errorMsg('Port')
        ## Read the response
        
        ## Parse the response
        
        ## Display the response
#        self.plot.add_s_data(data)
        pass
    
    def _idata(self):
        """ Retreive IDATA button function
        
        Commands ICM for IDATA, parses respnose and displays on graph
        
        Args:
            None
        Returns:
            None
        
        """
        print('idata')
        ## ***DEBUG ONLY ***
        update('idata')
        ## Send IDATA command to ICM
        try:
            assert(self.serial.serial.is_open == True)
            self.serial.serial.write(b"IDATA\n")
        except:
            self._errorMsg('Port')
        ## Read the response
        
        ## Parse the response
        
        ## Display the response
#        self.plot.add_i_data(data)
        
        pass
    def _retreive_file(self):
        """ Retreive ICM Param File 
        
        Command ICM to return Param file, display in parameter chart
        
        Args:
            None
        Returns:
            None
        """
        print('retreive file')
        pass
        
    def _clear_data(self):
        """ Clear ICM SDATA and IDATA
        Clears all data from SDATA and IDATA (CANNOT BE RETREIVED)
        
        Args:
            None
        Returns:
            None        
        """
        print('clear data')
        self.plot.clear_data()
        pass
        
    def _errorMsg(self,value):
        """ Display Error Message
        
        Displays an pop-up error message for selectable invalid command or error
        
        Args:
            value (str): Type of error message to display
        Returns:
            None       
        """
        if(value == 'File'):
            message = "Invalid File"
        if(value == 'Port'):
            message = "Serial Port Not Open"
            
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Error")
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
    
    def help(self):
        """ Display the help menu
        
        Displays the help menu for the ICM GUI
        
        Args:
            None
        Returns:
            None       
        """
        #print("Help")
        message = """<b>ICM-GUI v{}</b> <br> Interface Control Module Graphical User Interface <br>
            Copyright (c) 2017 NOAA <br>Pacific Marine Environmental Lab <br>
            Licensed under the terms of the MIT License<br>
            <br>
            Created by Matthew Casari<br>
            <br>
            For bugs and feature requests, please go to the PMEL Github Webpage.
            
            
            """
        ## Add the version number into the message 
        message = message.format(self._version_string)
        
        ## Grab the PMEL Logo
        pixmap = QtGui.QPixmap("PMEL.png").scaled(150,150)

        
        
        msgBox = QMessageBox()
        msgBox.setWindowTitle("About ")
        msgBox.setTextFormat(Qt.RichText)
        msgBox.setIconPixmap(pixmap)
        msgBox.setText(message)
        msgBox.setStandardButtons(QMessageBox.Ok)
        msgBox.exec_()
        
        

    def _save_file(self):
        """ Save parameter file to disk
        Save the user configurable parameter file to disk (working directory)
        
        Args:
            None
        Returns:
            None
        """
        
        params = self.param.system_params.getValues()
        path = os.getcwd()
        generateICMFile(params,os.path.join(path,'Test.txt'))



## Start Qt event loop unless running in interactive mode or using pyside.
        
        
def update(graph='both'):
    """ Update loop for debugging 
    ***REMOVE FOR PRODUCTION
    This loop generates random data for the idata and sdata graphs
    
    """
#    print("Time's up")
    global idx,win
    
    if(graph =='both' or graph == 'sdata'):
        slen = np.random.randint(1,60)
    if(graph =='both' or graph == 'idata'):
        ilen = np.random.randint(1,60)

    ## Create time (x) data
    tt = dt.datetime.utcnow()
    td = dt.timedelta(milliseconds=100)
    
    if(graph == 'sdata' or graph =='both'):
        sxvals = np.array(range(update.scounter,update.scounter+slen))
        update.scounter += slen
    if(graph == 'idata' or graph == 'both'):
        ixvals = np.array(range(update.icounter,update.icounter+ilen))
        update.icounter += ilen


    if(graph == 'both' or graph == 'sdata'):
        sdata = pd.DataFrame(np.random.randint(0,10,size=[slen,4]), columns=['Wind Ave', 'Std', 'Min', 'Max'])
        sdata['timestamp[utc]'] = sxvals
        win.plot.add_s_data(sdata)

    
    if(graph =='both' or graph == 'idata'):
        idata = pd.DataFrame(np.random.randint(0,100,size=[ilen,2]), columns=['A','B'])
        idata['timestamp[utc]'] = ixvals   
        win.plot.add_i_data(idata)



    
    
if __name__ == '__main__':
    import sys
    global idx
    idx = 0
    app = QtGui.QApplication([])
    
    if(False):
        timer = QTimer()
        timer.timeout.connect(update)
        timer.start(500)

    win = MainWindow()

        
    win.resize(1280,720)
    win.setWindowTitle('ICM Interface')
    win.show()
    

    update.counter = 0
    update.scounter = 0
    update.icounter = 0

    sys.exit(app.exec_())
    
    
#    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
#        #QtGui.QApplication.instance().exec_()
#
#        
#        win = MainWindow()
#
#        
#        win.resize(1280,720)
#        win.setWindowTitle('ICM Interface')
#        win.show()
#        
#
#
#        update.counter = 0
#
#        sys.exit(app.exec_())


