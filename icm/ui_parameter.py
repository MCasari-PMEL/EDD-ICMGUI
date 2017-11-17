from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
from pyqtgraph import GraphicsLayoutWidget

from ICM_parameters import *
import pyqtgraph as pg
import sys, os, glob, json
 

class ICMParams(QWidget):        
    def __init__(self,version='1.0.0'):
        super(ICMParams,self).__init__()
        
        self._import_params()
        self._create_params()
        self._create_param_tree()
        self._create_master()
        self._create_tabs()
        self._create_checkboxes()
        self._display()
        ver = {'MASTER':{'Firmware Version':version}}
        
    
         
        self._set_statechanged()
        
    def UpdateParams(self,filename):
        ## Check to see if it is a valid file
        cwd = os.getcwd()
        os.chdir('..')
        jfile = filename + ".json"
        filepath = os.path.join(os.getcwd(),'sensors')
        filepath = os.path.join(filepath,'json')
        filepath = os.path.join(filepath,jfile)
        os.chdir(cwd)
        if(os.path.exists(filepath)==False):
            raise IOError('File Not Found')
            return
        
        self._import_params(filename)
        self._refresh_params()
        
        
    def _refresh_params(self):
        self._create_params()
        self._MASTER_t.clear()
        self._COM1_t.clear()
        self._COM2_t.clear()
        self._COM3_t.clear()
        self._MASTER_t.addParameters(self._MASTER_p)
        self._COM1_t.addParameters(self._COM1_p)
        self._COM2_t.addParameters(self._COM2_p)
        self._COM3_t.addParameters(self._COM3_p)
        self._set_statechanged()
        QApplication.processEvents()
        
    def _display(self):
        
        vbox = QVBoxLayout()

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.master)
        
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.addWidget(self.grid)

        
        splitter3 = QSplitter(Qt.Vertical)
        splitter3.addWidget(self.tabs)

        
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(splitter1)
        self.splitter.addWidget(splitter2)
        self.splitter.addWidget(splitter3)
        
        vbox.addWidget(self.splitter)
        
        self.setLayout(vbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        



    def _import_params(self,name="Default"):
        curdir = os.getcwd()
        os.chdir('..')
        path = os.path.join(os.getcwd(),'sensors')
        jpath = os.path.join(path,'json')
        jfile = os.path.join(jpath,name+".json")
        
        os.chdir(curdir)
        
        ## Import JSON file
        with open(jfile,encoding='utf-8') as json_data: 
            d = json.load(json_data)
        
        self.master_params = d['MASTER']
        self.com_params = d['COM']
        return
        
    def _create_params(self):
        
        ## Create the parameters
        self._MASTER_p = Parameter.create(name='MASTER',type='group',children=self.master_params)
        self._COM1_p = Parameter.create(name='COM1',type='group',children=self.com_params['COM1'])
        self._COM2_p = Parameter.create(name='COM2',type='group',children=self.com_params['COM2'])
        self._COM3_p = Parameter.create(name='COM3',type='group',children=self.com_params['COM3'])
                
    
        ## Create the inclusive parameter tree
        self.system_params = Parameter.create(name='System',type='group')
        self.system_params.addChild(self._MASTER_p)
        self.system_params.addChild(self._COM1_p)
        self.system_params.addChild(self._COM2_p)
        self.system_params.addChild(self._COM3_p)
    
    def _create_param_tree(self):
        
        ## Set up the COM1 Parameter Tree
        self._COM1_t = ParameterTree()
        self._COM1_t.setParameters(self._COM1_p,showTop=True)
        self._COM1_t.setWindowTitle('COM1 Parameter Tree')
        
        ## Set up the COM2 Parameter Tree
        self._COM2_t = ParameterTree()
        self._COM2_t.setParameters(self._COM2_p,showTop=True)
        self._COM2_t.setWindowTitle('COM2 Parameter Tree')
        
        ## Set up the COM3 Parameter Tree
        self._COM3_t = ParameterTree()
        self._COM3_t.setParameters(self._COM3_p,showTop=True)
        self._COM3_t.setWindowTitle('COM3 Parameter Tree')
        
    def _update_param_tree(self):
        self._COM1_t.clear()
        self._COM2_t.clear()
        self._COM3_t.clear()
        self._COM1_t.addParameters(self._COM1_p)
        self._COM2_t.addParameters(self._COM2_p)
        self._COM3_t.addParameters(self._COM3_p)
        QApplication.processEvents()
    def _set_statechanged(self):
        ## Set the state changed connections
        self._MASTER_p.sigTreeStateChanged.connect(self._MASTER_change)
        self._COM1_p.sigTreeStateChanged.connect(self._COM_change)
        self._COM2_p.sigTreeStateChanged.connect(self._COM_change)
        self._COM3_p.sigTreeStateChanged.connect(self._COM_change)
      
        
    def _create_master(self):       
        ## Set up the Master Parameter Tree
        self.master = QWidget()
        self._MASTER_t = ParameterTree(parent=self.master)
        self._MASTER_t.setParameters(self._MASTER_p,showTop=True)
        self._MASTER_t.setWindowTitle('MASTER Parameter Tree')
        
        ## Resize the widget
        self.master.setMinimumHeight(len(self._MASTER_p.getValues())*20+60)
        
        
    def _create_tabs(self):
        
        ## Create the tab widget and add the parameter trees
        self.tabs = QTabWidget()
        self.tabs.addTab(self._COM1_t,"COM1")
        self.tabs.addTab(self._COM2_t,"COM2")
        self.tabs.addTab(self._COM3_t,"COM3")
        
        ## Resize the widget
        self.tabs.setMinimumWidth(self.tabs.sizeHint().width())
        self.tabs.setMaximumWidth(self.tabs.sizeHint().width()+30)


        
    def _create_checkboxes(self):
        
        ## Create 3 checkboxes
        self._COM1_check = QCheckBox()
        self._COM2_check = QCheckBox()
        self._COM3_check = QCheckBox()
        
        ## Create a grid Widget
        self.grid = QWidget()
        
        ## Create a gridlayout with the grid widget as the parent
        self._check_grid = QGridLayout(self.grid)

        ## Add labels and buttons to the widget
        self._check_grid.addWidget(QLabel("Include the following"),0,0,1,5)
        self._check_grid.addWidget(QLabel("COM1"),1,0)
        self._check_grid.addWidget(QLabel("COM2"),1,1)
        self._check_grid.addWidget(QLabel("COM3"),1,2)
        self._check_grid.addWidget(self._COM1_check,2,0)
        self._check_grid.addWidget(self._COM2_check,2,1)
        self._check_grid.addWidget(self._COM3_check,2,2)

        ## Set the minimum column widths
        self._check_grid.setColumnMinimumWidth(0,5)
        self._check_grid.setColumnMinimumWidth(1,5)
        self._check_grid.setColumnMinimumWidth(2,5)
        self._check_grid.setColumnMinimumWidth(3,5)
        
        
        ## Add connect to checkboxes
        self._COM1_check.clicked.connect(lambda state,x=0:self._check_COM_clicked(state,x))
        self._COM2_check.clicked.connect(lambda state,x=1:self._check_COM_clicked(state,x))
        self._COM3_check.clicked.connect(lambda state,x=2:self._check_COM_clicked(state,x))
        
        ## Set Checked
        self._COM1_check.setChecked(True)
        self._COM2_check.setChecked(True)
        self._COM3_check.setChecked(True)

        ## Fix the height of the checkbox widget
        self.grid.setFixedHeight(self.grid.sizeHint().height())
        
    def disable_checkboxes(self,value=True):
        self._COM1_check.setDisabled(value)
        self._COM2_check.setDisabled(value)
        self._COM3_check.setDisabled(value)
        return

    def disable_parameters(self,value=True):
        pass
#        self._COM1_p.unblockTreeChangeSignal()
#        self._COM2_p.unblockTreeChangeSignal()
#        self._COM3_p.unblockTreeChangeSignal()
#        
#        for item in self._COM1_p.names:
#            self._COM1_p[item].setEnabled(False)
#        self._COM1_p.setReadonly(True)
#        self._COM1_p.setOpts(readonly=True)
#        self._update_param_tree()
#        QApplication.processEvents()
        
    def _update_com_param_dict(self,params):
        temp = []
        columnCnt = 0
        idx = 0
        hasCommand = 0
        for items in params:
            #temp.append(items)
            if(items.name() == 'Name'):
                temp.append({'name':'Name','type':'str','value':items.value()})
                if(self._valid_name(items.value())==False):
                    temp[-1]['value'] = "NAME"
            elif(items.name() == 'Prefix'):
                temp.append({'name':'Prefix','type':'str','value':items.value()})
                if(self._valid_prefix(items.value())==False):
                     temp[-1]['value'] = "Prefix"
            elif(items.name() == 'Serial Port'):
                temp.append({'name':'Serial Port','type':'str','value':items.value()})
                if(self._valid_serialport(items.value())==False):
                     temp[-1]['value'] = 0
            elif(items.name() == 'Baud Rate'):
                temp.append({'name':'Baud Rate','type':'list',
                'values':['1200','2400','4800','9600','19200','28800','57600','115200'],
                'value':int(items.value())})
                
                if(self._valid_baudrate(items.value())==False):
                     temp[-1]['value'] = 9600
            elif(items.name() == 'Warmup Time'):
                temp.append({'name':'Warmup Time','type':'int','value':items.value()})
                if(self._valid_warmup(items.value())==False):
                     temp[-1]['value'] = 0
            elif(items.name() == 'Sample Start Time'):
                temp.append({'name':'Sample Start Time','type':'str','value':items.value()})
                if(self._valid_samplestart(items.value())==False):
                     temp[-1]['value'] = "00:00:00"
            elif(items.name() == 'Sample Interval'):
                temp.append({'name':'Sample Interval','type':'str','value':items.value()})
                if(self._valid_sampleinterval(items.value())==False):
                     temp[-1]['value'] = "00:00:00"
            elif(items.name() == 'Sample Period'):
                temp.append({'name':'Sample Period','type':'str','value':items.value()})
                if(self._valid_sampleperiod(items.value())==False):
                     temp[-1]['value'] = "00:00:00"
            elif(items.name() == 'Sample Rate'):
                temp.append({'name':'Sample Rate','type':'int','value':items.value()})
                if(self._valid_samplerate(items.value())==False):
                     temp[-1]['value'] = 1
            elif(items.name() == 'Power Switch'):
                temp.append({'name':'Power Switch','type':'list','values':{"OFF":0,"ON":1},'value':items.value()})
                if(self._valid_powerswitch(items.value())==False):
                     temp[-1]['value'] = 0
            elif(items.name() == 'Command'):
                temp.append({'name':'Command','type':'list','values':{"N":0,"Y":1},'value':items.value()})
                if(self._valid_command(items.value())==False):
                     temp[-1]['value'] = 0
                hasCommand = temp[-1]['value']
            elif(items.name() == 'cmd'):
                temp.append({'name':'cmd','type':'str','value':items.value()})
                if((hasCommand==0) or (self._valid_cmd(items.value())==False)):
                     temp[-1]['value'] = "NA"
            elif(items.name() == 'header'):
                temp.append({'name':'header','type':'str','value':items.value()})
                if(self._valid_header(items.value())==False):
                     temp[-1]['value'] = ""
            elif(items.name() == 'format'):
                temp.append({'name':'format','type':'str','value':items.value()})
                if(self._valid_format(items.value())==False):
                     temp[-1]['value'] = ""
                columnCnt = len(items.value())
            elif(items.name().find('column') != -1):
                temp.append({'name':'column[{}]'.format(idx),'type':'str','value':items.value()})
                if(idx >= columnCnt):
                    del(temp[-1])
                idx += 1
        for i in range(idx,columnCnt):
            temp.append({'name':'column[{}]'.format(i),'type':'str','value':""})
        temp.append({'name':'=end'})
        return temp 

    def _valid_name(self,name):
        status = False
        if(type(name) == str):
            status = True
        return status
    def _valid_prefix(self,prefix):
        status = False
        if(type(prefix) == str):
            status = True
        return status
    def _valid_serialport(self,port):
        status = False
        if(type(port) == str):
            if((int(port)>=0) and (int(port)<=255)):
                status = True;
        return status
    def _valid_baudrate(self,baud):
        status = False
        if(['1200','2400','4800','9600','19200','28800','57600','115200'].index(baud) >= 0):
            status = True
        return status
    def _valid_warmup(self,warmup):
        return True
    def _valid_samplestart(self,start):
        return True
    def _valid_sampleinterval(self,interval):
        return True
    def _valid_sampleperiod(self,period):
        return True
    def _valid_samplerate(self,rate):
        return True
    def _valid_powerswitch(self,switch):
        return True
    def _valid_command(self,command):
        return True
    def _valid_cmd(self,cmd):
        return True
    def _valid_header(self,header):
        return True
    def _valid_format(self,frmt):
        return True
    def _MASTER_change(self):
        pass
    def _COM_change(self,com):
        ## Update COM1
        temp = self._update_com_param_dict(self._COM1_p)
        del(self.com_params['COM1'])
        self.com_params['COM1']=temp
                       
        ## Update COM2
        temp = self._update_com_param_dict(self._COM2_p)
        del(self.com_params['COM2'])
        self.com_params['COM2']=temp
                       
        ## Update COM3
        temp = self._update_com_param_dict(self._COM3_p)
        del(self.com_params['COM3'])
        self.com_params['COM3']=temp
                       
        ## Refresh all params
        
        self._refresh_params()
        
    def _check_COM_clicked(self,state,x):
        self.tabs.setTabEnabled(x,state)
        
# Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    class MainWindow(QtGui.QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("ICM Parameter")
            layout = QtGui.QVBoxLayout()
            
            self.params = ICMParams('1.0.0')
            self.params.disable_checkboxes(True)
            self.params.disable_parameters(True)
            layout.addWidget(self.params)

                
            widget = QtGui.QWidget()
            widget.setLayout(layout)

            self.setCentralWidget(widget)
        
            #self.setGeometry(200,200,400,550)

    app = QtGui.QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    
    print(window.params)
    
    
    app.exec_()

