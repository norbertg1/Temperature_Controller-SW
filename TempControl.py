from typing import Text
from tkinter import ttk
import tkinter as tk
from Settings import *
from Communication import serial_communication
import struct
import crcmod
import sys

window = tk.Tk()
 
window.title("Temperature Controller")
window.minsize(600,400)
serial_port = serial_communication()        #This is the constructor for serial_port class in Communication.py
settings = Settings_(serial_port)

def SetTemp():
    SetTemp = int(float(SetTemp_var.get())*10)
    settings.data[0] = SetTemp
    settings.data[2] = 1                    #Set menu to start heating or cooling
    settings.SendSettings()
    return None

def OpenSettings():
    settings.OpenSettingsWindow()
    return None

def ReadCurrentTemp():
    measurements_raw = serial_port.Read(16)
    try:
       measurements = struct.unpack('ffff', measurements_raw)
       CurrentTemp_label.configure(text= str(round(measurements[0], 3)) + " ℃")
       Voltage_label.configure(text= str(round(measurements[1], 3)) + " V")
       Amps_label.configure(text= str(round(measurements[2], 3)) + " A")
       Power_label.configure(text= str(round(measurements[3], 3)) + " W")
    except:
        # I/O Error, add error handler
        CurrentTemp_label.configure(text= str(0.0) + " ℃")
    window.after(200, ReadCurrentTemp)
    return None

def OpenSerial():
    print("Selected Option: {}".format(value_inside.get()))
    if(serial_port.Open(value_inside.get())):
        if(settings.ReadSettings()):
            SetTemp_entry.delete(0, END)
            SetTemp_entry.insert(0, round(settings.data[0]/10,3))
            tkinter.Label(window, text = "Port OK, Device OK", font= ("default", "12", "bold")).grid(column= 4, row = 0)
        else:
            tkinter.Label(window, text = "Port Ok, Device Failed", font= ("default", "12", "bold")).grid(column= 4, row = 0)
    else:
        tkinter.Label(window, text = "Port Failed", font= ("default", "12", "bold")).grid(column= 4, row = 0)
    return None


ttk.Label(window, text = "Target Temperature").grid(column = 0, row = 1)
CurrentTemp_label   = ttk.Label(window, text = None, font= ("default", "24", "bold") )
Voltage_label       = ttk.Label(window, text = None, font= ("default", "12"))
Amps_label          = ttk.Label(window, text = None, font= ("default", "12"))
Power_label         = ttk.Label(window, text = None, font= ("default", "12" ))

CurrentTemp_label.place(x = 150, y = 40)
Voltage_label.place(x = 350, y = 30)
Amps_label.place(x = 350, y = 48)
Power_label.place(x = 350, y = 66)

SetTemp_var     = tk.StringVar()
SetTemp_entry   = ttk.Entry(window, width = 15, textvariable = SetTemp_var)
SetTemp_entry.grid(column = 0, row = 2)
setTempButton   = ttk.Button(window, text = "SET", command = SetTemp)
setTempButton.grid(column= 0, row = 3)

ttk.Button(window, text = "Options", command = OpenSettings).grid(column= 3, row = 0)
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


window.after(300, ReadCurrentTemp)
window.mainloop()