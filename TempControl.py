from typing import Text
from tkinter import ttk
import tkinter as tk
from Settings import *
from Communication import serial_communication
import struct
import crcmod

window = tk.Tk()
 
window.title("Temperature Controller")
window.minsize(600,400)
serial_port = serial_communication()        #This is the constructor for serial_port class in Communication.py

def SetTemp():
    SetTemp = int(SetTemp_var.get())*10
    crc32 = 0
    SetTemp_raw = struct.pack("ssssisssssssssss", b"T",b"T",b"T",b"T",SetTemp,b"T",b"T",b"T",b"T",b"T",b"T",b"T",b"T",b"T",b"T",b"T")
    #SetTemp_raw = struct.pack("sis", b"TTT",SetTemp,b"TTTTTTTTTTTT")

    print(SetTemp_raw.hex())
    crc32 = crcmod.predefined.mkCrcFun('crc-32-mpeg')(SetTemp_raw)
    #SetTemp_raw = struct.pack("4s4s4si4s4s4s4s4s4s4s4s4s4s4sI", b"T",b"T",b"T",SetTemp,b"T",b"T",b"T",b"T",b"T",b"T",b"T",b"T",b"T",b"T",b"T",crc32)
    #struct.pack_into("I", SetTemp_raw, 60, crc32)
    print(SetTemp_raw.hex())
    serial_port.Write(SetTemp_raw)
    #send on serial port out

def OpenSettings():
    settings = Settings_(serial_port)
    return None

def ReadCurrentTemp():
    current_temp = (999.999)
    current_temp_raw = serial_port.Read(4)
    try:
       current_temp = struct.unpack('f', current_temp_raw)
       currentTemp_label.configure(text= str(round(current_temp[0], 3)) + " ℃")
    except:
        # I/O Error, add error handler
        current_temp = 0.0  
        currentTemp_label.configure(text= str(current_temp) + " ℃")
    window.after(200, ReadCurrentTemp)
    return None

def OpenSerial():
    print("Selected Option: {}".format(value_inside.get()))
    if(serial_port.Open(value_inside.get())):
        tkinter.Label(window, text = "Ok", font= ("default", "12", "bold")).grid(column= 3, row = 0)
    else:
        tkinter.Label(window, text = "Failed", font= ("default", "12", "bold")).grid(column= 3, row = 0)
    return None

ttk.Label(window, text = "Enter Temperature").grid(column = 0, row = 1)
currentTemp_label = ttk.Label(window, text = None, font= ("default", "24", "bold") )
currentTemp_label.place(x = 150, y = 40)

SetTemp_var = tk.StringVar()
ttk.Entry(window, width = 15, textvariable = SetTemp_var).grid(column = 0, row = 2)
setTempButton = ttk.Button(window, text = "SET", command = SetTemp)
setTempButton.grid(column= 0, row = 3)

ttk.Button(window, text = "Options", command = OpenSettings).grid(column= 4, row = 0)
i=0

ports = serial.tools.list_ports.comports()
devices = []
for port in sorted(ports):
    devices.append(port.device)

value_inside = tkinter.StringVar(window)
ChooseSerialMenu = OptionMenu(window, value_inside ,*devices )
ChooseSerialMenu.grid(column= 0, row = 0)
setSerialButton = tkinter.Button(window, text = "Open", command = OpenSerial)
setSerialButton.grid(column= 1, row = 0)


window.after(200, ReadCurrentTemp)
window.mainloop()