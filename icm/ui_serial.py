from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout)
 
import sys, serial, glob
 
class SerialPort(QDialog):
 
    def __init__(self):
        super(SerialPort, self).__init__()
        
        self.serial = serial.Serial()
        
        self._find_available_ports()
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

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Open | QDialogButtonBox.Close)
#        self.buttonBox = QDialogButtonBox(connectButton | disconnectButton)
        self.buttonBox.accepted.connect(self._connect_to_port)
        self.buttonBox.rejected.connect(self._disconnect_from_port)
 
    def _create_form_group_box(self):
        self._create_combo_boxes()
        self.formGroupBox = QGroupBox("Serial Port Setting")
        self.layout = QFormLayout()
        self.layout.addRow(QLabel("Port:"), self._port_combo)
        self.layout.addRow(QLabel("Baud:"), self._baud_combo)
        self.layout.addRow(QLabel("Data bits:"), self._databits_combo)
        self.layout.addRow(QLabel("Parity bits:"), self._parity_combo)
        self.layout.addRow(QLabel("Stop bits:"), self._stopbits_combo)
        self.formGroupBox.setLayout(self.layout)

    def _create_combo_boxes(self):
        ## Create the serial PORT combo box
        self._port_combo = QComboBox()
        for port in self._portnames:
            self._port_combo.addItem(port)
        
        ## Create the serial BAUDRATE combo box
        self._baud_combo = QComboBox()
        for baud in self.serial.BAUDRATES:
            self._baud_combo.addItem(str(baud))
        self._baud_combo.setCurrentIndex(self.serial.BAUDRATES.index(9600))
            
        ## Create the DATABITs combo box
        self._databits_combo = QComboBox()
        for bits in self.serial.BYTESIZES:
            self._databits_combo.addItem(str(bits))
        self._databits_combo.setCurrentIndex(self.serial.BYTESIZES.index(8))
        
        ## Create the PARITY combo box
        self._parity_combo = QComboBox()
        for parity in self.serial.PARITIES:
            self._parity_combo.addItem(parity)
        self._parity_combo.setCurrentIndex(self.serial.PARITIES.index('N'))
            
        ## Create the STOPBITS combo box
        self._stopbits_combo = QComboBox()
        for sbits in self.serial.STOPBITS:
            self._stopbits_combo.addItem(str(sbits))
        self._stopbits_combo.setCurrentIndex(self.serial.STOPBITS.index(1))
        
    def _find_available_ports(self):        
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i+1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported Platform')
        self._portnames = []

        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                self._portnames.append(port)
            except (OSError,serial.SerialException):
                pass 
            
    def _connect_to_port(self):
        ## Set the serial control values
        self.serial.port = self._port_combo.currentText()
        self.serial.baud = int(self._baud_combo.currentText())
        self.serial.parity = self._parity_combo.currentText()
        self.serial.bytesize = int(self._databits_combo.currentText())
        self.serial.stopbits = float(self._stopbits_combo.currentText())
        self.serial.timeout = 0.5
        
        ## Open the Port
        self.serial.open()
        
        ## Set the status flag
        self._check_connected()
 
    def _disconnect_from_port(self):
        ## Close the port
        self.serial.close()
        ## Set the status flag
        self.connected = self.serial.isOpen()
        
    def _check_connected(self):
        self.connected = self.serial.isOpen()
    
    
    def read(self,length=0):
        ## Make sure the port is connected
        self._check_connected()
        
        ## If connected, read the data and decode it
        if self.connected == True:
            self.rx_buffer = []
            
            ## If rx length is 0, read all data on the port
            if length == 0:
                data = self.serial.read()
            else:
                data = self.serial.read(length)
                
            self.rx_buffer = data.decode('utf-8')
        else:
            raise ValueError("Serial Port not connected")
            
    def write(self,string):
        ## Make sure the port is connected
        self._check_connected()
        
        ## If connected, write the converted (byte string) data
        if self.connected == True:
            self.serial.write(string)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog = SerialPort()
    sys.exit(dialog.exec_())