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

from ICM_parameters import *
import pyqtgraph as pg
import sys, os, glob
 

class ICMParams(QWidget):        
    def __init__(self,version='1.0.0'):
        super(ICMParams,self).__init__()
        
        self._import_params(version)
        self._create_params()
        self._create_master()
        self._create_tabs()
        self._create_checkboxes()
        self._display()
        ver = {'MASTER':{'Firmware Version':version}}
        
        
        t = self._MASTER_p.children()
        t[0]['Firmware Version'] = version
         
        self._set_statechanged()

    def _display(self):
        
        vbox = QVBoxLayout()
        
        master = QFrame()
        master.setFrameShape(QFrame.StyledPanel)

        buttons = QFrame()
        buttons.setFrameShape(QFrame.StyledPanel)
        
        
        com = QFrame()
        com.setFrameShape(QFrame.StyledPanel)
    
        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self._MASTER_t)
        #splitter1.setMinimumHeight(100)
        splitter1.setMinimumSize(250,100)
        splitter1.resize(splitter1.sizeHint())
        
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(self.grid)
        #splitter2.setMinimumHeight(75)
        splitter2.setMinimumSize(250,75)
        
        splitter3 = QSplitter(Qt.Vertical)
        splitter3.addWidget(self.tabs)
        splitter3.resize(splitter3.sizeHint())

        
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(splitter1)
        self.splitter.addWidget(splitter2)
        self.splitter.addWidget(splitter3)
        
        vbox.addWidget(self.splitter)
        #vbox.addWidget(self.splitter2)
        #vbox.addWidget(self.splitter3)
        self.setLayout(vbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        



    def _import_params(self,version):
        if(version == '1.0.0'):
            self.master_params = []
            self.com_params = []
            self.master_params = master_params_1_0_0
            self.com_params = com_params_1_0_0
        else:
            self.master_params = []
            self.com_params = []
            self.master_params = master_params_1_0_0
            self.com_params = com_params_0_0_1
        
        
    def _create_params(self):
        
        ## Create the parameters
#        self._MASTER_p = Parameter.create(name='Master',type='group',children=self.master_params)
        self._MASTER_p = Parameter.create(name='MASTER',type='group',children=self.master_params)
        self._COM1_p = Parameter.create(name='COM1',type='group',children=self.com_params)
        self._COM2_p = Parameter.create(name='COM2',type='group',children=self.com_params)
        self._COM3_p = Parameter.create(name='COM3',type='group',children=self.com_params)
                
        
        ## Set up the Master Parameter Tree
        self._MASTER_t = ParameterTree()
        self._MASTER_t.setParameters(self._MASTER_p,showTop=False)
        self._MASTER_t.setWindowTitle('MASTER Parameter Tree')
        
        #self.master = QWidget(self._MASTER_t)
        #self.master.setMinimumHeight(75)
        
        ## Set up the COM1 Parameter Tree
        self._COM1_t = ParameterTree()
        self._COM1_t.setParameters(self._COM1_p,showTop=False)
        self._COM1_t.setWindowTitle('COM1 Parameter Tree')
        
        ## Set up the COM2 Parameter Tree
        self._COM2_t = ParameterTree()
        self._COM2_t.setParameters(self._COM2_p,showTop=False)
        self._COM2_t.setWindowTitle('COM2 Parameter Tree')
        
        ## Set up the COM3 Parameter Tree
        self._COM3_t = ParameterTree()
        self._COM3_t.setParameters(self._COM3_p,showTop=False)
        self._COM3_t.setWindowTitle('COM3 Parameter Tree')
        
        
        ## Create the inclusive parameter tree
        self.system_params = Parameter.create(name='System',type='group')
        self.system_params.addChild(self._MASTER_p)
        self.system_params.addChild(self._COM1_p)
        self.system_params.addChild(self._COM2_p)
        self.system_params.addChild(self._COM3_p)
        
        
    def _set_statechanged(self):
                ## Set the state changed connections
        self._MASTER_p.sigTreeStateChanged.connect(self._MASTER_change)
        self._COM1_p.sigTreeStateChanged.connect(self._COM1_change)
        self._COM2_p.sigTreeStateChanged.connect(self._COM2_change)
        self._COM3_p.sigTreeStateChanged.connect(self._COM3_change)
        
    def _create_master(self):
        mlayout = QHBoxLayout()
        mlayout.addWidget(self._MASTER_t)
        self.master = QWidget()
        
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

        self._check_grid.addWidget(QLabel("Include the following"),0,0,1,5)
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
        t = self._MASTER_p.children()
        if t[0]['Firmware Version'].count('.') != 2:
            return
        
        
        self._COM1_p.clearChildren()
        self._COM2_p.clearChildren()
        self._COM3_p.clearChildren()
        
        #del self.master_params
        #del self.com_params
        self.master_params = []
        self.com_params = []
        if(t[0]['Firmware Version'] == '1.0.0'):
            self._import_params('1.0.0')
        else:
            self._import_params('0.0.1')
        
        self._create_params()
        self._display()
        self.show()
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
            
            self.params = ICMParams('1.0.0')

            
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

