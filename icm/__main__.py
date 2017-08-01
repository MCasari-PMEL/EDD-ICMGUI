#!/usr/bin/env python

# -*- coding: utf-8 -*-

import sys, os, time, serial, json
import numpy as np

import pyqtgraph as pg
import pyqtgraph.console 
from PyQt5.QtCore import pyqtSignal, QObject
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *

from icm.ui_clock import *
from icm.ui_createfile import *
from icm.ui_parameter import *
from icm.ui_serial import *

from icm.ui_qicmgui import Ui_QIcmGuiMainWindow


class Communicate(QObject):
    closeApp = pyqtSignal()
    
class QIcmGuiMainWindow(QtGui.QMainWindow, Ui_QIcmGuiMainWindow):
    """ ICMGUI Main Window """
    def __init__(self,parent=None):
        #Initialize the GUI
        super().__init__(parent)
        self.setupUi(self)
        
        
        #Create a communication event to close the window
        self.c = Communicate()
        
        ## Create docks and place them in the window
        self.cd = SerialWidget(self.gridLayout_2)

    #@QtCore.slot()
    def closeEvent(self,event):
        
        pass

def main():
    app = QtGui.QApplication([])
    window = QIcmGuiMainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()
    
#if __name__ != "__main__":
#    raise ImportError('this module should not be imported')
    
    
