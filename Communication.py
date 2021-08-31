import serial.tools.list_ports
import serial
import time
import struct

class serial_communication():
    def __init__(self):
        self.ser = serial.Serial(
        port=None,
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
        )
        return None
    
    def Open(self, com_port):
        self.ser = serial.Serial(
        port=com_port,
        baudrate=115200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
        )
        return self.ser.isOpen()
    
    def Write(self, data):
        if self.ser.isOpen():
            self.ser.write((data + '\r\n').encode())
            time.sleep(1)
        return None

    def Read(self, size):
        if self.ser.isOpen():
            data = self.ser.read(size)
            self.ser.flushInput()
            print (data)
            return data
            
        return 999.999