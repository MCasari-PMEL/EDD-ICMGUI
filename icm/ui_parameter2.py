# -*- coding: utf-8 -*-
"""
This example demonstrates the use of pyqtgraph's parametertree system. This provides
a simple way to generate user interfaces that control sets of parameters. The example
demonstrates a variety of different parameter types (int, float, list, etc.)
as well as some customized parameter types

"""


#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui


#app = QtGui.QApplication([])
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
import sys

subparams = [   {'name':'Name','type':'str','value':'NAME'},
                {'name':'Prefix','type':'str','value':'PREFIX'},
                {'name':'Serial Port','type':'str','value':'XXXX'},
                {'name':'Baud Rate','type':'list','values':['1200','2400','4800','9600','19200','28800','57600','115200'],'value':'9600'},
                {'name':'Warmup Time','type':'int','value':12000},
                {'name':'Sample Start Time','type':'str','value':'00:00:00'},
                {'name':'Sample Interval','type':'str','value':'00:01:00'},
                {'name':'Sample Period','type':'str','value':'00:00:20'},
                {'name':'Sample Rate','type':'int','value':1},
                {'name':'Power Switch','type':'int','value':1},
                {'name':'Command','type':'str','value':'0'},
                {'name':'cmd','type':'str','value':""},
                {'name':'header','type':'str','value':'$'},
                {'name':'format','type':'str','value':'ccfcfcfc'},
                {'name':'column[0]','type':'str','value':'$'},
                {'name':'column[1]','type':'str','value':'C'},
                {'name':'column[2]','type':'str','value':'Heading'},
                {'name':'column[3]','type':'str','value':'P'},
                {'name':'column[4]','type':'str','value':'Pitch'},
                {'name':'column[5]','type':'str','value':'R'},
                {'name':'column[6]','type':'str','value':'Roll'},
                {'name':'column[7]','type':'str','value':'*'},
                {'name':'=end'}
                ]


params = [
    {'name': 'MASTER','type':'group','children': [
        ##{'name':'System','type':'list','values':['Master','COM1','COM2','COM3'],'value':0},
        {'name':'PMEL Serial Number','type':'str','value':'XXXXXXXXXX'},
        {'name':'Firmware Version','type':'str','value':'XXXXXXXXXX'}
        ]},
    {'name':'COM1','type':'group','children':  subparams },
    {'name':'COM2','type':'group','children':  subparams },
    {'name':'COM3','type':'group','children':  subparams } ]

class SystemParams(QtGui.QWidget):

    def __init__(self,*args,**kwargs):
        super(SystemParams,self).__init__(*args,**kwargs)

        self.p = Parameter.create(name='params', type='group', children=params)

        self.p.sigTreeStateChanged.connect(self.change)
        #self.p.param('Save/Restore functionality', 'Save State').sigActivated.connect(self.save)
        #self.p.param('Save/Restore functionality', 'Restore State').sigActivated.connect(self.restore)

        ## Create two ParameterTree widgets, both accessing the same data
        self.t = ParameterTree()
        self.t.setParameters(self.p, showTop=False)
        self.t.setWindowTitle('pyqtgraph example: Parameter Tree')





        win = QtGui.QWidget()
        layout = QtGui.QGridLayout()
        self.setLayout(layout)
        layout.addWidget(QtGui.QLabel("ICM Parameters"), 0,  0, 1, 2)
        layout.addWidget(self.t, 1, 0, 1, 1)

        win.show()
        win.resize(350,550)
        win.setMinimumHeight(550)

    ## If anything changes in the tree, print a message
    def change(self,param, changes):
        for param, change, data in changes:
            path = self.p.childPath(param)
            if path is not None:
                childName = '.'.join(path)
            else:
                childName = param.name()


    def save(self):
        
        global state
        state = p.saveState()
    
    def restore(self):
        global state
        add = self.p['Save/Restore functionality', 'Restore State', 'Add missing items']
        rem = self.p['Save/Restore functionality', 'Restore State', 'Remove extra items']
        p.restoreState(state, addChildren=add, removeChildren=rem)
        
    def update(self,parameters):
        print(parameters)
        self.p.setValue(parameters)
        pass


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    class MainWindow(QtGui.QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("ICM Parameter")
            layout = QtGui.QVBoxLayout()
            
            self.params = SystemParams()

            
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

