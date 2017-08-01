#from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
#        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
#        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
#        QVBoxLayout, QTabWidget, QWidget, QCheckBox)

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph import GraphicsLayoutWidget

import pyqtgraph as pg
import sys, os, glob
 

master_params = [
    {'name': 'MASTER','type':'group','children': [
        ##{'name':'System','type':'list','values':['Master','COM1','COM2','COM3'],'value':0},
        {'name':'PMEL Serial Number','type':'str','value':'XXXXXXXXXX'},
        {'name':'Firmware Version','type':'str','value':'XXXXXXXXXX'}
        ]} ]


com_params = [   {'name':'Name','type':'str','value':'NAME'},
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

class ICMParams(QWidget):
#    def __init__(self):
#        super(ICMParams,self).__init__()
#        
#        self._create_params()
#        self._create_tabs()
#        self._create_checkboxes()
#        
#        win = QWidget()
#        layout = QGridLayout()
#        #layout = QVBoxLayout()
#        self.setLayout(layout)
#        #layout.addWidget(QLabel("ICM Parameter"))
#        layout.addWidget(self._MASTER_t,0,0,1,1)
##        layout.addWidget(QHor)
#        layout.addLayout(self._check_grid,2,0,1,1)
#        layout.addWidget(self.tabs)
##        layout.addWidget(self._COM1_t,2,0,1,1)
#
#        win.show()
#        win.resize(350,550)
#        win.setMinimumHeight(500)
#        #mainLayout = QVBoxLayout()
        
        
    def __init__(self):
        super(ICMParams,self).__init__()
        
        self._create_params()
        self._create_tabs()
        self._create_checkboxes()
        
        
        vbox = QVBoxLayout()
        
        master = QFrame()
        master.setFrameShape(QFrame.StyledPanel)
        #master.setLayout(self._MASTER_t)
        buttons = QFrame()
        buttons.setFrameShape(QFrame.StyledPanel)
        
        com = QFrame()
        com.setFrameShape(QFrame.StyledPanel)
    
        self.splitter = QSplitter(Qt.Vertical)
        #self.splitter.addWidget(master)
        self.splitter.addWidget(self._MASTER_t)
        self.splitter.addWidget(self.grid)
        #self.splitter.addWidget(self.)
        self.splitter.addWidget(self.tabs)
        
        vbox.addWidget(self.splitter)
        self.setLayout(vbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        
        self.show()

        #win.setMinimumHeight(500)
        
        
    def _create_params(self):
        
        ## Create the parameters
        self._MASTER_p = Parameter.create(name='Master',type='group',children=master_params)
        self._COM1_p = Parameter.create(name='params',type='group',children=com_params)
        self._COM2_p = Parameter.create(name='params',type='group',children=com_params)
        self._COM3_p = Parameter.create(name='params',type='group',children=com_params)
        
        ## Set the state changed connections
        self._MASTER_p.sigTreeStateChanged.connect(self._MASTER_change)
        self._COM1_p.sigTreeStateChanged.connect(self._COM1_change)
        self._COM2_p.sigTreeStateChanged.connect(self._COM2_change)
        self._COM3_p.sigTreeStateChanged.connect(self._COM3_change)
        
        ## Set up the Master Parameter Tree
        self._MASTER_t = ParameterTree()
        self._MASTER_t.setParameters(self._MASTER_p,showTop=False)
        self._MASTER_t.setWindowTitle('MASTER Parameter Tree')
        
        self.master = QWidget(self._MASTER_t)
        ## Set up the Master Parameter Tree
        self._COM1_t = ParameterTree()
        self._COM1_t.setParameters(self._COM1_p,showTop=False)
        self._COM1_t.setWindowTitle('COM1 Parameter Tree')
        
        ## Set up the Master Parameter Tree
        self._COM2_t = ParameterTree()
        self._COM2_t.setParameters(self._COM2_p,showTop=False)
        self._COM2_t.setWindowTitle('COM2 Parameter Tree')
        
        ## Set up the Master Parameter Tree
        self._COM3_t = ParameterTree()
        self._COM3_t.setParameters(self._COM3_p,showTop=False)
        self._COM3_t.setWindowTitle('COM3 Parameter Tree')
        
        
    def _create_tabs(self):
        
        self.tabs = QTabWidget()
        self.tabs.addTab(self._COM1_t,"COM1")
        self.tabs.addTab(self._COM2_t,"COM2")
        self.tabs.addTab(self._COM3_t,"COM3")
        
    def _create_checkboxes(self):
        self._COM1_check = QCheckBox()
        self._COM2_check = QCheckBox()
        self._COM3_check = QCheckBox()
        
        self.grid = QWidget()
        
        self._check_grid = QGridLayout(self.grid)

        self._check_grid.addWidget(QLabel("Include the following"),0,0,1,1)
        self._check_grid.addWidget(QLabel("COM1"),1,0)
        self._check_grid.addWidget(QLabel("COM2"),1,1)
        self._check_grid.addWidget(QLabel("COM3"),1,2)
        self._check_grid.addWidget(self._COM1_check,2,0)
        self._check_grid.addWidget(self._COM2_check,2,1)
        self._check_grid.addWidget(self._COM3_check,2,2)

        self._check_grid.setColumnMinimumWidth(0,5)
        self._check_grid.setColumnMinimumWidth(1,5)
        self._check_grid.setColumnMinimumWidth(2,5)
        self._check_grid.setColumnMinimumWidth(3,5)
        
        
    def _MASTER_change(self):
        pass
    def _COM1_change(self):
        pass
    def _COM2_change(self):
        pass
    def _COM3_change(self):
        pass

# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    class MainWindow(QtGui.QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("ICM Parameter")
            layout = QtGui.QVBoxLayout()
            
            self.params = ICMParams()

            
            layout.addWidget(self.params)

                
            widget = QtGui.QWidget()
            widget.setLayout(layout)

            self.setCentralWidget(widget)
        
            self.setGeometry(200,200,400,550)

    app = QtGui.QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    print(window.params)
    
    
    app.exec_()

