# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 08:26:55 2017

@author: casari
"""

import pyqtgraph as pg
from pyqtgraph.dockarea import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

import numpy as np
import pandas as pd
import datetime as dt



class Graph(QWidget):
    def __init__(self,num_iVars,num_sVars):
        super(Graph,self).__init__()

        ## Create the dataframes
        self.sdata = pd.DataFrame([])
        self.idata = pd.DataFrame([])

        ## Set the number of variables for this plot
        self.num_iVars = num_iVars
        self.num_sVars = num_sVars
        
        
        ## Create the Iridium and Standard Plots
        self.ipw = pg.PlotWidget()
        self.spw = pg.PlotWidget()

        ## Add the plots to the widget
        self._add_i_plot(num_iVars)
        self._add_s_plot(num_sVars)
        
        ## Create the DockArea
        self.plotarea = QWidget()
        
        ## Create the docks
        self._create_plot_dock()
        

        ## Update the plot so everything jives
        self.updateViews()
        
        ## Connect plot resizing so everything continues to jive
        self._iPlot[0].vb.sigResized.connect(self.updateViews)
        self._sPlot[0].vb.sigResized.connect(self.updateViews)
        
        ## Create the main layout and show the widget
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self._area)
        self.setLayout(mainLayout)
        self.show()


    def _add_i_plot(self,iVars):
        """ Create iData Plot 
        
        Creates the actual iData plot used in the dock.
        
        Args:
            iVars (int): Number of iData variables (# of curves)
        Returns:
            None
        """
        self._iCurve =[[]]*iVars
        self._iPlot = []
        
        ## Create the and the curves data variables
        for i in range(0,iVars):
            self._iCurve[i] = pg.PlotCurveItem([])
            self._iCurve[i].setPen(pg.intColor(i))
            if(i == 0):
                self._iPlot.append(self.ipw.plotItem)
                self._iPlot[0].setLabels(left='axis0')
                
            else:
                 self._iPlot.append(pg.ViewBox())
                 self._iPlot[0].scene().addItem(self._iPlot[i])
                 self._iPlot[0].getAxis('right').linkToView(self._iPlot[i])
                 self._iPlot[i].setXLink(self._iPlot[0])


        self._iPlot[0].plot([])
        for i in range(0,iVars):
            self._iPlot[i].addItem(self._iCurve[i])    


    def _add_s_plot(self,sVars):
        """ Create sData Plot 
        
        Creates the actual sData plot used in the dock.
        
        Args:
            sVars (int): Number of sData variables (# of curves)
        Returns:
            None
        """
        self._sCurve =[[]]*sVars
        self._sPlot = []
        
        ## Create the and the curves data variables
        for i in range(0,sVars):
            self._sCurve[i] = pg.PlotCurveItem([])
            self._sCurve[i].setPen(pg.intColor(i))
            if(i == 0):
                self._sPlot.append(self.spw.plotItem)
                self._sPlot[0].setLabels(left='axis0')
            else:
                 self._sPlot.append(pg.ViewBox())
                 self._sPlot[0].scene().addItem(self._sPlot[i])
                 self._sPlot[0].getAxis('right').linkToView(self._sPlot[i])
                 self._sPlot[i].setXLink(self._sPlot[0])


        self._sPlot[0].plot([])
        for i in range(0,sVars):
            self._sPlot[i].addItem(self._sCurve[i])            
            
    def _plot_i_data(self,x,data,text):
        """ Plot iData values on graph
        
        Plots the continous series of iData values on the graph.
        
        Args:
            x (timestamp): Timestamp values for x-axis
            data (array):  Numpy array of data (rows contain individual data)
            text (list): List of row headings
        Returns:
            None
        """
        
        try:       
            for idx in range(0,len(data)):
                self._iCurve[idx].setData(x,data[idx])
        except:
            print("Error in iData: " + str(data[idx]))
            
    def add_i_data(self,data):
        """ Add data to running dataframe
        
        Adds idata in a pandas dataframe to the running sdata dataframe.  Plots
        full run
        
        Args:
            data (dataframe): Pandas d
            idx+=1
            
            
        legend.setParentItem(self.ipw)
            ataframe of sData
        
        Returns:
            None
        
        """
        self.idata = self.idata.append(data)
        
        x = np.array(self.idata['timestamp[utc]'])
        text = list(self.idata)
        ndata = np.array(self.idata.loc[:,self.idata.columns !='timestamp[utc]'])
        
        ## Setup legend if it doesn't exist
        if hasattr(self,'ilegend'):
            pass
        else:
            self.ilegend = pg.LegendItem()
            for idx in range(0,len(self._iCurve)):
                self.ilegend.addItem(self._iCurve[idx],text[idx])
                
            self.ilegend.setParentItem(self._iPlot[0])
        
        self._plot_i_data(x,ndata.T,text)  
        
        
    def _plot_s_data(self,x,data,text):
        """ Plot sData values on graph
        
        Plots the continous series of sData values on the graph.
        
        Args:
            x (timestamp): Timestamp values for x-axis
            data (array):  Numpy array of data (rows contain individual data)
            text (list): List of row headings
        Returns:
            None
        """
        
        try:       
            for idx in range(0,len(data)):
                self._sCurve[idx].setData(x,data[idx])
        except:
            print("Error in sData: " + str(data[idx]))
            
    def add_s_data(self,data):
        """ Add data to running dataframe
        
        Adds sdata in a pandas dataframe to the running sdata dataframe.  Plots
        full run
        
        Args:
            data (dataframe): Pandas dataframe of sData
        
        Returns:
            None
        
        """
        self.sdata = self.sdata.append(data)
        
        x = np.array(self.sdata['timestamp[utc]'])
        text = list(self.sdata)
        ndata = np.array(self.sdata.loc[:,self.sdata.columns !='timestamp[utc]'])
        
        ## Setup legend 
        if hasattr(self,'slegend'):
            pass
        else:
            self.slegend = pg.LegendItem()
            for idx in range(0,len(self._sCurve)):
                self.slegend.addItem(self._sCurve[idx],text[idx])
                
            self.slegend.setParentItem(self._sPlot[0])
            
        self._plot_s_data(x,ndata.T,text)                

    def _create_plot_dock(self):
        """ Create the Dock Area for both plots
        
        Creates a DockArea to Dock both iData and sData
        
        Args:
            None
        Returns:
            None
        """
        self._area = DockArea(self.plotarea)
        
        self.iDock = Dock("iData")
        self.sDock = Dock("sData")
        
        self._area.addDock(self.iDock,'top')
        self._area.addDock(self.sDock,'bottom')
        self.iDock.addWidget(self.ipw)
        self.sDock.addWidget(self.spw)
        

        
#    def clear_data(self):
#        self._iData = []
#        self._sData = []
    
     
    def updateViews(self):
        """
        Updates the plots so all curves fit in same area
        
        Args:
            None
        Returns:
            None
        """
        
        ## view has resized; update auxiliary views to match
        for i in range(1,len(self._sPlot)):
            self._sPlot[i].setGeometry(self._sPlot[0].vb.sceneBoundingRect())
            self._sPlot[i].linkedViewChanged(self._sPlot[0].vb,self._sPlot[i].XAxis)
        for i in range(1,len(self._iPlot)):
            self._iPlot[i].setGeometry(self._iPlot[0].vb.sceneBoundingRect())
            self._iPlot[i].linkedViewChanged(self._iPlot[0].vb,self._iPlot[i].XAxis)  



def update():
#    print(update.counter)
    global data, curve, count,dock,idx
    
    sdata = [] #np.random.normal(size=4)
    idata = []
#    
    sdata = pd.DataFrame(np.random.randint(0,10,size=[8,4]), columns=['Wind Ave', 'Std', 'Min', 'Max'])
    idata = pd.DataFrame(np.random.randint(0,100,size=[8,2]), columns=['A','B'])
    tt = dt.datetime.utcnow()
    td = dt.timedelta(milliseconds=100)
    

    
    xvals = np.array(range(update.counter,update.counter+8))
#    print(xvals)
    sdata['timestamp[utc]'] = xvals
    idata['timestamp[utc]'] = xvals
    dock.add_s_data(sdata)
    dock.add_i_data(idata)
#    dock.add_i_data(idata)
    update.counter += 8
    
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    global idx
    idx = 0
    
    ## Start the timer
    timer = QTimer()
    timer.timeout.connect(update)
    timer.start(3000)
    
    pg.mkQApp()
    
    ## Create the Dock object
    dock = Graph(2,4)

    ## Create fake data
#    idata = pd.DataFrame(np.random.randint(0,100,size=[8,4]), columns=['A', 'B', 'C', 'D'])
#    sdata = pd.DataFrame(np.random.randint(0,10,size=[8,4]), columns=['A', 'B', 'C', 'D'])
#    tt = dt.datetime.utcnow()
#    td = dt.timedelta(milliseconds=100)
#    
#    ts = []
#    for i in range(0,8):
##        ts.append(dt.datetime.timestamp(tt+i*td))
##        timestamp = dt.datetime.timestamp(tt+i*td)
#        timestring = dt.datetime.strftime((tt+i*td),"%M:%S.%f")[:-3]
##        dval = {timestamp,timestring}
#        ts.append(timestring)
##        print(ts)
##    ts = [tt,(tt+td),(tt+td*2),(tt+td*3),(tt+td*)]
##    xvals = dict(enumerate(timestring))
#    xvals = np.array(range(0,8))
#    sdata['timestamp[utc]'] = xvals
#    
#    ## Plot sData
#    dock.add_s_data(sdata)
    update.counter = 0
    
    sys.exit(app.exec_() )
    