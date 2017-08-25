# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 14:00:48 2017

@author: casari
"""

import pyqtgraph as pg
from pyqtgraph.dockarea import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

import numpy as np

#width_spin = [("Floating-point spin box, min=0, no maximum.", pg.SpinBox(value=5.0, bounds=[0, None]))]


class Graph(QWidget):
    def __init__(self,num_iVars,num_sVars):
        super(Graph,self).__init__()
#        self._iData = []
#        self._sData = []
        self.num_iVars = num_iVars
        self.num_sVars = num_sVars
        
        self._add_i_plot(num_iVars)
        self._add_s_plot(num_sVars)
        
        self.plotarea = QWidget()
        
        self._create_plot_dock()
        self._create_splitters()
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self._area)
        self.setLayout(mainLayout)
        self.show()


    def _add_i_plot(self,iVars):
        self._iCurve = []
        self._iData = []
        self._iPlot = []
        ## Create the and the curves data variables
        for i in range(0,iVars):
            self._iData.append(np.array([]))
            self._iCurve.append(pg.PlotCurveItem([]))

        self.ipw = pg.PlotWidget()
        self.ipw.setWindowTitle('Testing Testing')
        self._iPlot.append(self.ipw.plotItem)
        self._iPlot[0].setLabels(left='axis0')

        
        for i in range(1,iVars):
            self._iPlot.append(pg.ViewBox())
            if(i == 1):
                self._iPlot[0].showAxis('right')
                self._iPlot[0].scene().addItem(self._iPlot[1])
                self._iPlot[0].getAxis('right').linkToView(self._iPlot[1])
                self._iPlot[1].setXLink(self._iPlot[0])
                self._iPlot[0].getAxis('right').setLabel('Axis {}'.format(i))
            else:
                axis = pg.AxisItem('right')
                self._iPlot[0].layout.addItem(axis,2,i+1)
                self._iPlot[0].scene().addItem(self._iPlot[i])
                axis.linkToView(self._iPlot[i])
                self._iPlot[i].setXLink(self._iPlot[0])
                axis.setZValue(-1000)
                axis.setLabel('Axis {}'.format(i))

        self._iPlot[0].addItem(self._iCurve[0])
        for i in range(1,iVars):
            self._iPlot[i].addItem(self._iCurve[i])

    def _add_s_plot(self,sVars):
        self._sCurve = []
        self._sData = []
        self._sPlot = []
        ## Create the and the curves data variables
        for i in range(0,sVars):
            self._sData.append(np.array([]))
            self._sCurve.append(pg.PlotCurveItem([]))

        self.spw = pg.PlotWidget()
        self.spw.setWindowTitle('Testing Testing')
        self._sPlot.append(self.spw.plotItem)
        self._sPlot[0].setLabels(left='axis0')

        
        for i in range(1,sVars):
            self._sPlot.append(pg.ViewBox())
            if(i == 1):
                self._sPlot[0].showAxis('right')
                self._sPlot[0].scene().addItem(self._sPlot[1])
                self._sPlot[0].getAxis('right').linkToView(self._sPlot[1])
                self._sPlot[1].setXLink(self._sPlot[0])
                self._sPlot[0].getAxis('right').setLabel('Axis {}'.format(i))
            else:
                axis = pg.AxisItem('right')
                self._sPlot[0].layout.addItem(axis,2,i+1)
                self._sPlot[0].scene().addItem(self._sPlot[i])
                axis.linkToView(self._sPlot[i])
                self._sPlot[i].setXLink(self._sPlot[0])
                axis.setZValue(-1000)
                axis.setLabel('Axis {}'.format(i))

        self._sPlot[0].addItem(self._sCurve[0])
        for i in range(1,sVars):
            self._sPlot[i].addItem(self._sCurve[i])
            
    def _create_splitters(self):
        pass
        

    def _create_plot_dock(self):
        self._area = DockArea(self.plotarea)
        
        self.iDock = Dock("iData")
        self.sDock = Dock("sData")
        
        self._area.addDock(self.iDock,'top')
        self._area.addDock(self.sDock,'bottom')
        self.iDock.addWidget(self.ipw)
        self.sDock.addWidget(self.spw)
        
        #self.sDock.addWidget(self.sCurve)
        
        #self.iDock.addWidget(self._area)
    
    def add_iData(self,curveNum,data):
        self._iData[curveNum] = np.append(self._iData[curveNum],data)
        self._iCurve[curveNum].setData(data)

    def add_sData(self,curveNum,data):
        self._sData[curveNum] = np.append(self._sData[curveNum],data)
        self._sCurve[curveNum].setData(data)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    iLength = 8
    sLength = 3
    Graph = Graph(iLength,sLength)
    
    data = np.array([1,2,4,8,16,32])
    #data = 
#    try:
    for i in range(0,iLength):
        Graph.add_iData(i,data*(i+1))
       
    for s in range(0,sLength):
        Graph.add_sData(s,1/data*(s+1))
#    for i in range(0,sLength):
#        Graph.add_sData(i,data*(i+1))
        #Graph.changeLineWidth(0,2)
        #Graph.changeLineColor(0,[255,0,0])
#    except Exception as e:
#        print(e)
        
        Graph.show()
    sys.exit(app.exec_() )
    #sys.exit(Graph.exec_())