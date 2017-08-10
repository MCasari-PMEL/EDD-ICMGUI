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
from ui_createfile import *
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
        self.paramDock = Dock("System Parameters",size=(200,200))
        self.fileDock = Dock("Create File",size=(60,25))
        self.serialDock = Dock("Serial Port",size=(60,25))
        self.meatballDock = Dock("PMEL Logo",size=(60,25))

        self.area.addDock(self.headerDock,'top')
        self.area.addDock(self.plotDock,'bottom',self.headerDock)
        self.area.addDock(self.paramDock,'right',self.plotDock)
        self.area.addDock(self.fileDock,'right',self.paramDock)
        self.area.addDock(self.serialDock,'bottom',self.fileDock)
        self.area.addDock(self.meatballDock,'bottom',self.serialDock)
        
        
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
        self.plot = Graph(8,2)
        self.plotDock.addWidget(self.plot)
        
        
        ## Add System Parameters Widget
        self.param = ICMParams()
        self.paramDock.addWidget(self.param)
        
        
        ## Add Serial Port Widget
        self.serial = SerialPort()
        self.serialDock.addWidget(self.serial)
        
        ## Add Create File
        self.file_ = CreateFileWidget()
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
        
        
        self.connect_buttons()
        
        
        self.setFixedSize(1200,700)
        
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
            icmAct.triggered.connect( lambda checked,name=item['name']:self._read_param_file(name))
            icmMenu.addAction(icmAct)

            
        
        ## Add to Help menu
        helpMenu.addAction('About ICM Interface')
        helpMenu.triggered.connect(self.help)
        
    def _read_param_file(self,index):
        print(index)
        #icmMenu.addMenu('Test')
    def connect_buttons(self):
        
        self.file_.port_btn.clicked.connect(self.save_file)
        
    
    def help(self):
        #print("Help")
        message = """<b>ICM-GUI v{}</b> <br> Interface Control Module Graphical User Interface <br>
            Copyright (c) 2017 NOAA <br>Pacific Marine Environmental Lab <br>
            Licensed under the terms of the MIT License<br>
            <br>
            Created by Matthew Casari<br>
            <br>
            For bugs and feature requests, pleasge go to the PMEL Github Webpage.
            
            
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
        
        

    def save_file(self):
        
        params = self.param.system_params.getValues()
        path = os.getcwd()
        generateICMFile(params,os.path.join(path,'Test.txt'))



## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        #QtGui.QApplication.instance().exec_()

        app = QtGui.QApplication([])
        win = MainWindow()

        #win.setCentralWidget(area)
        win.resize(120,70)
        #win.resize(win.area.sizeHint())
        #win.resize(Q)
        win.setWindowTitle('ICM Interface')

        win.show()
        
        ## Add some test data
        iLength = 8
        sLength = 3
        data = np.array([1,2,4,8,16,32])
        try:
            for i in range(0,iLength):
                win.plot.add_iData(i,data*(i+1))
               
            for i in range(0,sLength):
                win.plot.add_sData(i,data*(i+1))
        except Exception as e:
            print(e)


        

        sys.exit(app.exec_())


