# -*- coding: utf-8 -*-
"""
Created on Fri Aug  4 14:00:48 2017

@author: casari
"""

import pyqtgraph as pg
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

import numpy as np

#width_spin = [("Floating-point spin box, min=0, no maximum.", pg.SpinBox(value=5.0, bounds=[0, None]))]


class Graph(QWidget):
    def __init__(self,num_iVars,num_sVars):
        super(Graph,self).__init__()
        
        self.num_iVars = num_iVars
        self.num_sVars = num_sVars
        
        self._addPlotUi(num_iVars,num_sVars)
        self._addCurveFeatures(num_iVars,num_sVars)
        self._addClearButton()
        
        self._change_i_Features()
        self._change_s_Features()
            
        #mainLayout = QVBoxLayout()
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.win,0,0,5,5)
        mainLayout.addLayout(self.iFeatureLayout,0,5,1,1)
        mainLayout.addLayout(self.sFeatureLayout,1,5,1,1)
        #mainLayout.setColumnMinimumWidth(5,80)
        mainLayout.setColumnStretch(5,1)
        
        
        mainLayout.addWidget(self.clearButton,4,5,2,2)
        
        self.setLayout(mainLayout)
        self.show()
        
        
    def _addPlotUi(self,iVars,sVars):
        #self.win = pg.GraphicsWidget(title="Basic plotting examples")
        self.win = pg.GraphicsWindow()
        
        self.iPlot = self.win.addPlot(title='iData')
        self.win.nextRow()
        self.sPlot = self.win.addPlot(title='sData')
        
        #self.iData = np.array([])
        #self.sData = np.array([])
        self.iData = []
        self.sData = []
        self.iCurve = []
        self.sCurve = []
        
        
        for i in range(0,iVars):
            self.iCurve.append(self.iPlot.plot())
            self.iData.append(np.array([]))
        for s in range(0,sVars):
            self.sCurve.append(self.sPlot.plot())
            self.sData.append(np.array([]))  
            
            
    def _addCurveFeatures(self,iVars,sVars):
        self.iFeatureLayout = QGridLayout()
        self.sFeatureLayout = QGridLayout()
        
        mainFont = QFont('Serif',14)
        
        self.iFeatureLayout.addWidget(QLabel("iData Graph Features",font=QFont("Times",10,QFont.Bold)),0,0,1,4)
        self.sFeatureLayout.addWidget(QLabel("sData Graph Features",font=QFont("Times",10,QFont.Bold)),0,0,1,4)
        
        self._iFeatureWidth = []
        self._iFeatureColor = []
        self._sFeatureWidth = []
        self._sFeatureColor = []
        
        
        for i in range(0,iVars):
            #self.iFeatureLayout.addWidget(pg.SpinBox(value=0.2,bounds=[0.1,5.0]))
            #label = QLabel("Line {}".format(i)
            #label.setFont(QFont("Times",12,QFont.Bold))
            #self.iFeatureLayout.addWidget(label,i+1,0,1,1)
            self.iFeatureLayout.addWidget(QLabel("Line {}".format(i),width=25),i+1,0,1,1)
            self._iFeatureWidth.append(pg.SpinBox(value=1.0,bounds=[0.2,5.0],step=0.1))
            self._iFeatureWidth[i].setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            self._iFeatureWidth[i].setMaximumWidth(40)
            self._iFeatureWidth[i].sigValueChanged.connect(self._change_i_Features)
            self.iFeatureLayout.addWidget(self._iFeatureWidth[i],i+1,1,1,1)
            self.iFeatureLayout.addWidget(QLabel("Width",width=30),i+1,2,1,1)
            self._iFeatureColor.append(pg.ColorButton(color=[200,200,200]))
            self._iFeatureColor[i].setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            self._iFeatureColor[i].sigColorChanged.connect(self._change_i_Features)
            self.iFeatureLayout.addWidget(self._iFeatureColor[i],i+1,3,1,1)
            self.iFeatureLayout.addWidget(QLabel("Color"),i+1,4,1,1)
        #self.sFeatureLayout = QVBoxLayout()
        for i in range(0,sVars):
            self.sFeatureLayout.addWidget(QLabel("Line {}".format(i),width=25),i+1,0,1,1)
            self._sFeatureWidth.append(pg.SpinBox(value=1.0,bounds=[0.2,5.0],step=0.1))
            self._sFeatureWidth[i].setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            self._sFeatureWidth[i].setMaximumWidth(40)
            self._sFeatureWidth[i].sigValueChanged.connect(self._change_s_Features)
            self.sFeatureLayout.addWidget(self._sFeatureWidth[i],i+1,1,1,1)
            self.sFeatureLayout.addWidget(QLabel("Width".format(i),width=30),i+1,2,1,1)
            self._sFeatureColor.append(pg.ColorButton(color=[200,200,200]))
            self._sFeatureColor[i].setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
            self._sFeatureColor[i].sigColorChanged.connect(self._change_s_Features)
            self.sFeatureLayout.addWidget(self._sFeatureColor[i],i+1,3,1,1)
            self.sFeatureLayout.addWidget(QLabel("Color"),i+1,4,1,1)
            
        self.iFeatureLayout.minimumSize()
    def _addClearButton(self):
        self.clearButton = QPushButton('Clear Data/Graph',self)
        self.clearButton.clicked.connect(self.clearData)
        self.clearButton.setMaximumSize(self.clearButton.sizeHint())
        self.clearButton.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
    def add_iData(self,curveNum,data=[]):
        self.iData[curveNum] = np.append(self.iData[curveNum],data)
        self.iCurve[curveNum].setData(self.iData[curveNum])
        
    def add_sData(self,curveNum,data=[]):
        self.sData[curveNum] = np.append(self.sData[curveNum],data)
        self.sCurve[curveNum].setData(self.sData[curveNum])
  
    def _change_i_Features(self):
        for i in range(self.num_iVars):
            iColor = self._iFeatureColor[i].color()
            iWidth = self._iFeatureWidth[i].value()
            self.iCurve[i].setPen(color=iColor,width=iWidth)
 
    def _change_s_Features(self):
        for i in range(self.num_sVars):
            sColor = self._sFeatureColor[i].color()
            sWidth = self._sFeatureWidth[i].value()
            self.sCurve[i].setPen(color=sColor,width=sWidth)
        
    def clearData(self):
        ## Delete the data and set the curve
        for i in range(0,self.num_iVars):
            self.iData[i] = []
            self.iCurve[i].clear()
        
        for s in range(0,self.num_sVars):
            self.sData[s] = []
            self.sCurve[s].clear()
        
    
    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    iLength = 8
    sLength = 3
    Graph = Graph(iLength,sLength)
    
    data = np.array([1,2,4,8,16,32])
    #data = 
    try:
        for i in range(0,iLength):
            Graph.add_iData(i,data*(i+1))
           
        for i in range(0,sLength):
            Graph.add_sData(i,data*(i+1))
        #Graph.changeLineWidth(0,2)
        #Graph.changeLineColor(0,[255,0,0])
    except Exception as e:
        print(e)
        
        Graph.show()
        sys.exit(app.exec_() )
#sys.exit(Graph.exec_())