from pyqtgraph.Qt import QtCore
import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import serial


pg.setConfigOptions(antialias=True)

class SerialPort:
    """ Serial Port Widget """
    
    def __init__(self,layout):
        
        if not isinstance(layout,pg.LayoutWidget):
            raise ValueError("layout must be QGridLayout")
            
        self.layout = layout
        
        self.layout.addLabel("Port")
        
        
    

if __name__ == "__main__":            
    class MainWindow(QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("Main Test Window")
            layout = pg.LayoutWidget()
            #layout.addLabel("Test",0,0)
            self.SerialPort = SerialPort(layout)

            
            #layout.addWidget(self.SerialPort)

            
            widget = QWidget()
            widget.setLayout(layout)

            self.setCentralWidget(widget)
        
            self.setGeometry(200,200,300,300)


            self.SerialPort.set_timer()

    app = QApplication(sys.argv)

    #window = SensorType()
    window = MainWindow()
    window.show()


    app.exec_()