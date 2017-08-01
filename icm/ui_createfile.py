# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 06:53:02 2017

@author: casari
"""

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import sys
import serial



class CreateFileWidget(QWidget):

    

    def __init__(self,*args,**kwargs):
        super(CreateFileWidget,self).__init__(*args,**kwargs)


        layout = QGridLayout()

        #Create the delete local file checkbox
        self.save_box = QCheckBox(u"Save Copy of File")
        self.save_box.setStatusTip(u"Check to Save a copy of the output file locally")
        self.save_box.setChecked(True)
        
        # Push file to target checkbox
        self.load_box = QCheckBox(u"Push File to Target")
        self.load_box.setStatusTip(u"Check to Load File on Target")
        self.load_box.setChecked(True)
        
        #Setup the Connect to Port button
        self.port_btn = QPushButton(u"Create ICM File",self)
        self.port_btn.setCheckable(True)
        self.port_btn.setStatusTip("Connect to the Serial Port")
        self.port_btn.clicked.connect(self.create_btn_clicked)

        self.port_btn.setFixedWidth(165)
        self.port_btn.setFont(QFont("Droid Sans",11))


        

        
        layout.addWidget(self.save_box,0,0)
        layout.addWidget(self.load_box,1,0)
        layout.addWidget(self.port_btn,2,0,2,1)
        
        layout.setSizeConstraint(QLayout.SetFixedSize)
        #layout.SetMinimumSize(QLayout.sizeHint)
        
        self.setLayout(layout)

        self.show()
        
        
    def create_btn_clicked(self):
        #print("Clicked")
        pass
        
        
if __name__ == "__main__":            
    class MainWindow(QMainWindow):

        def __init__(self,*args,**kwargs):
            super(MainWindow,self).__init__(*args,**kwargs)

            self.setWindowTitle("Main Test Window")
            layout = QVBoxLayout()
            self.SerialPort = CreateFileWidget()

            
            layout.addWidget(self.SerialPort)

            
            widget = QWidget()
            widget.setLayout(layout)

            self.setCentralWidget(widget)
        
            self.setGeometry(200,200,300,300)



    app = QApplication(sys.argv)

    #window = SensorType()
    window = MainWindow()
    window.show()


    app.exec_()
