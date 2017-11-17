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
#        self._iCurve = []
#        self._iData = []
#        self._iPlot = []
        ## Create the and the curves data variables
#        for i in range(0,iVars):
#            self._iData.append(np.array([]))
#            self._iCurve.append(pg.PlotCurveItem([]))

        self.ipw = pg.PlotWidget()
        self.ipw.setWindowTitle('Testing Testing')
#        self._iPlot.append(self.ipw.plotItem)
#        self._iPlot[0].setLabels(left='axis0')
#        self._iPlot.append(pg.ViewBox())

#        self.ipw



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
        self._sPlot.append(pg.ViewBox())
        



            
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
        
    def clear_data(self):
        self._iData = []
        self._sData = []
    
    def add_iData(self,x,data,text):
        """ Add iData to Plot
        
        Takes a numpy array of the form
        [[a0,a1,a2,...,an],
         [b0,b1,b2,...,bn],
         ...
         [z0,z1,z2,...,zn]]
        
        where each letter represents a time series and 0 is the first in the series
        
        Args:
            x (str): Timeseries values for x-axis
            data: Numpy array (as shown above)
            text: Text headers for each data series
        Returns:
            None
        
        """
        for d in data:
            self.ipw.addPlot(d)
            
            
    def add_sData(self,curveNum,data):
        self._sData[curveNum] = np.append(self._sData[curveNum],data)
        self._sCurve[curveNum].setData(data)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    iLength = 8
    sLength = 3
    Graph = Graph(iLength,sLength)
    
    
    sdata1 = '@@@3294,gill_b,wind001,2017/06/22,13:49:00,00:02:00\n218,290,10,11,12\n207,310,13,14,15\n232,390,16,17,18'
    idata1 = '@@@3294,gill_b,170622 14:49:00,-0.00,0.0,-0.01,0.1,10\n \
             gill_b,170622 14:51:00,0.10,0.2,0.30,0.4,50'
    
#    data = np.array([1,2,4,8,16,32])
    
    x = np.array(['1','2'])
    text = ['wind_speed[m/s]','wind_dir[deg]','heading[deg]','pitch[deg]','roll[deg]']
    
    data = np.array([[0.218,290,10,0,1.1,1.2],[0.207,310,13,1,1.4,1.5],[0.232,390,16,2,1.7,1.8],[0.128,326,10,3,1.1,1.2]])
    #data = 
#    try:
    for i in range(0,iLength):
        Graph.add_iData(i,data*(i+1))
       
    for s in range(0,sLength):
        Graph.add_sData(s,1/data*(s+1))
    for i in range(0,sLength):
        Graph.add_sData(i,data*(i+1))
#        Graph.changeLineWidth(0,2)
#        Graph.changeLineColor(0,[255,0,0])
#    except Exception as e:
#        print(e)
        
        Graph.show()
    sys.exit(app.exec_() )
    #sys.exit(Graph.exec_())