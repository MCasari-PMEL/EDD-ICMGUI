# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 14:18:56 2017

@author: casari
"""


import pyqtgraph as pg
from PyQt5.QtCore import pyqtSignal, QObject
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.Point import Point
from pyqtgraph.dockarea import *
import pyqtgraph.console

import numpy as np
import os
import sys
import serial
import json 

#from ics_file_generator import generateICMFile, parseParameters
from ics_file_generator import *
from ics_file_interpreter import *
from createfile_button_widget import CreateFileWidget
##from ics_file_generator import *
from parameter_widget import SystemParams
from serial_widget import SerialWidget


class Communicate(QObject):
    closeApp = pyqtSignal()

class MainWindow(QtGui.QMainWindow):

    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)

        ## Create a communication event to close the window
        self.c = Communicate()
        self.c.closeApp.connect(self.close)

        ## Create docks, place them into the window one at a time.
        ## Note that size arguments are only a suggestion; docks will still have to
        ## fill the entire dock area and obey the limits of their internal widgets.
        self.area = DockArea()

        self.d0 = Dock("Description",size=(200,50))
        self.d1 = Dock("System Parameters",size=(100,400))
        self.d2 = Dock("Create File",size=(60,25))
        self.d3 = Dock("PMEL Logo",size=(60,25))
        self.d4 = Dock("Serial Port",size=(60,80))


        self.area.addDock(self.d0,'top')
        self.area.addDock(self.d1,'bottom',self.d0)
        self.area.addDock(self.d4,'right',self.d1)
        self.area.addDock(self.d2,'bottom',self.d4)
        self.area.addDock(self.d3,'bottom',self.d2)

                ## Add widgets into each dock
        ## GUI Description
        self.w0 = pg.LayoutWidget()
        self.w0.setAutoFillBackground(True)
        palette = self.w0.palette()
        #palette.setColor(QtGui.QPalette.Window,QtGui.QColor('black'))
        label = QtGui.QLabel(""" ICM File Generator """)
        font = QtGui.QFont( "Helvetica", 18)
        font.setBold(True)
        label.setFont(font)
        label.setStyleSheet("color: black")
        label.setAlignment(QtCore.Qt.AlignCenter)
        self.w0.addWidget(label, row=0, col=0)
        self.d0.addWidget(self.w0)
        self.d0.hideTitleBar()


         
         
        ## System Parameters
        self.w1 = SystemParams()
        self.d1.addWidget(self.w1)

        ## SERIAL PORT Widget
        self.w4 = SerialWidget()
        self.d4.addWidget(self.w4)
        
        ## UTC CLOCK Widget
        self.w2 = CreateFileWidget()
        self.d2.addWidget(self.w2)
        self.w2.port_btn.clicked.connect(self.create_icm_file)

        

         ## MEATBALL
        self.w3 = pg.LayoutWidget()
        pic = QtGui.QLabel()
        pixmap = QtGui.QPixmap("PMEL.png")
        pic.setPixmap(pixmap)
        pic.setScaledContents(True)
        pic.setMaximumSize(150,150)
        self.w3.addWidget(pic, row=0, col=0)
        self.d3.addWidget(self.w3)
        self.d3.hideTitleBar()



        ## System Event Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(100)

        ## Add File Menu with open file and save file
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QtGui.QAction( QtGui.QIcon( os.path.join('icons','disk--arrow.png')), "Open File...",self)
        open_file_action.setStatusTip("Open from file")
        open_file_action.triggered.connect(self.open_file)
        file_menu.addAction(open_file_action)
        
        save_file_action = QtGui.QAction( QtGui.QIcon( os.path.join('icons','disk--pencil.png')), "Save File...",self)
        save_file_action.setStatusTip("Save File As")
        save_file_action.triggered.connect(self.save_file)
        file_menu.addAction(save_file_action)

        self.setCentralWidget(self.area)

    def create_icm_file(self):
        ## Get the current path and file
        path = os.getcwd()
        file = os.path.join(path,'ICM.txt')

        ## Create the ICM file
        generateICMFile(self.w1.p.getValues(),file)

        ## If the Load System box is checked, push it down
        ## over the serial port (if the port is open
        if(self.w2.load_box.isChecked()==True):
            if(self.w4.ser.isOpen()):
                with open(file,'r') as f:
                    for line in f:
                        temp = line[:-1]
                        temp += "\r\n"
                        self.w4.ser.write(temp.encode())

        if(self.w2.save_box.isChecked() == False):
            deleteICMFile(file)

            
    def open_file(self):
        filename, _ = QtGui.QFileDialog.getOpenFileName(self,"Open file", "",
                                                  "Text File (*.txt);;"
                                                  "All files (*.*)")

        #self.w1.p.restoreState()
        #parameters = interpretICMFile(self.w1.p.getValues(),filename)
        #self.w1.p.saveState()
        #self.w1.p.update(parameters)
        #self.w1.p = parameters
        
    def save_file(self):
        filename, _ = QtGui.QFileDialog.getSaveFileName(self, "Save Page As","",
                                                  "Text File (*.txt);;"
                                                  "All files (*.*)")

        ## Create the ICM file
        generateICMFile(self.w1.p.getValues(),filename)
        
        t1 = self.w1.p.saveState()
        filename, _ = QtGui.QFileDialog.getSaveFileName(self, "Save Page As","",
                                                  "JSON (*.json);;"
                                                  "All files (*.*)")
        with open(filename,'w') as f:
            f.write(json.dumps(t1,sort_keys=True,indent=4,separators=(',',':')))

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        #QtGui.QApplication.instance().exec_()

        app = QtGui.QApplication([])
        win = MainWindow()

        #win.setCentralWidget(area)
        win.resize(500,600)
        win.setWindowTitle('ICM Interface')

        win.show()

        sys.exit(app.exec_())
