from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout)
 
import sys, serial, glob
 
class DeviceStatus(QDialog):
 
    def __init__(self):
        super(DeviceStatus, self).__init__()

        
        self._create_form_group_box()
        self._create_buttons()
        
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)
 
        self.setWindowTitle("ICM Serial Port")
        
    def _create_buttons(self):
        
#        connectButton = QAbstractButton('Connect')
#        disconnectButton = QAbstractButton('Disconnect')

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Apply)
#        self.buttonBox = QDialogButtonBox(connectButton | disconnectButton)
        self.buttonBox.accepted.connect(self._connect_to_device)

 
    def _create_form_group_box(self):
        self.formGroupBox = QGroupBox("Device Status")
        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Port:"))
        self.layout.addRow(QLabel("Baud:"))
        self.layout.addRow(QLabel("Data bits:"))
        self.layout.addRow(QLabel("Parity bits:"))
        self.layout.addRow(QLabel("Stop bits:"))
        self.formGroupBox.setLayout(self.layout)


            
    def _connect_to_device(self):
        print("Connect")
        
        ## Set the status flag
        self._check_connected()
    
    def _create_device_status(self):
         ## Create the serial PORT combo box
        self._port_combo = QComboBox()
        for port in self._portnames:
            self._port_combo.addItem(port)

    def _update_device_status(self):
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = DeviceStatus()
    sys.exit(dialog.exec_())