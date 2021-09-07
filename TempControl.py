from graph import graphicon
from typing import Text
from tkinter import ttk
import tkinter as tk
from Settings import *
from Communication import serial_communication
import struct
import sys
import test
import matplotlib
from matplotlib.animation import FuncAnimation
from tkinter import messagebox

matplotlib.use('TkAgg')




window = tk.Tk()
window.title("Temperature Controller")
window.minsize(600,600)
serial_port = serial_communication()        #This is the constructor for serial_port class in Communication.py
settings    = Settings_(serial_port, window)
graph       = graphicon(window)

def SetTemp():
    SetTemp = int(float(SetTemp_var.get())*10)
    graph.setTargetTempline(SetTemp/10)
    settings.data[Settings_.TargetTemp] = SetTemp
    settings.data[Settings_.MenuNumber] = 1                    #Set menu to start heating or cooling
    if settings.SendSettings() is True: settings.DeviceStatus.status("Device OK", True)
    else: settings.DeviceStatus.status("Device Error", False)
    return None

def SetTemponEnter(event):
    SetTemp()

def OpenSettings():
    settings.OpenSettingsWindow()
    return None

def ReadCurrentTemp():
    try :
        measurements_raw = serial_port.Read(24)
        try:
            crc32 = crcmod.predefined.mkCrcFun('crc-32-mpeg')(measurements_raw[0:20])
            measurements = struct.unpack('fffffI', measurements_raw)
            if(crc32 == measurements[5]):
                CurrentTemp_label.configure(text= str(round(measurements[0], 3)) + " ℃")
                PowerPercent_label.configure(text= str(round(measurements[4], 2)) + " %")
                Voltage_label.configure(text= str(round(measurements[1], 3)) + " V")
                Amps_label.configure(text= str(round(measurements[2], 3)) + " A")
                Power_label.configure(text= str(round(measurements[3], 3)) + " W")
                graph.updatexy(measurements[0])
                animation.event_source.start()
                #settings.DeviceStatus.status("Device OK", True)
        except:
            # I/O Error, add error handler
            settings.DeviceStatus.status("Device Error", False)
            #CurrentTemp_label.configure(text= str(0.0) + " ℃")
    except:
        SerialStatus(False)
        settings.DeviceStatus.status("Device Error", False)
    window.after(200, ReadCurrentTemp)
    return None

def OpenSerial():
    print("Selected Option: {}".format(value_inside.get()))
    if(serial_port.Open(value_inside.get())):
        SerialStatus(True)
        if(settings.ReadSettings()):
            SetTemp_entry.delete(0, END)
            SetTemp_entry.insert(0, round(settings.data[Settings_.TargetTemp]/10,3))
            graph.setTargetTempline(settings.data[Settings_.TargetTemp]/10)
            settings.DeviceStatus.status("Device OK", True)
        else:
            settings.DeviceStatus.status("Device Error", False)
    else:
        SerialStatus(False)
    return None

def SerialStatus(stat):
    if stat is True:    Port_label.config(text = "Port OK,", font= ("default", "12", "bold"), fg="green")
    if stat is False:   Port_label.config(text = "Port Error", font= ("default", "12", "bold"), fg="red")

def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        settings.__del__()
        window.quit()

Port_label = tkinter.Label(window)
Port_label.grid(column= 4, row = 0)
Port_label.config(text = "Port Error", font= ("default", "12", "bold"), fg="red")
#tkinter.Label(window, text = "Port OK,", font= ("default", "12", "bold"), fg="green").grid(column= 4, row = 0)
ttk.Label(window, text = "Target Temperature").grid(column = 0, row = 1)
CurrentTemp_label   = ttk.Label(window, text = None, font= ("default", "24", "bold") )
PowerPercent_label  = ttk.Label(window, text = None, font= ("default", "16") )
Voltage_label       = ttk.Label(window, text = None, font= ("default", "12"))
Amps_label          = ttk.Label(window, text = None, font= ("default", "12"))
Power_label         = ttk.Label(window, text = None, font= ("default", "12" ))

CurrentTemp_label.place(x = 150, y = 40)
PowerPercent_label.place(x = 180, y = 80 )
Voltage_label.place(x = 360, y = 30)
Amps_label.place(x = 360, y = 48)
Power_label.place(x = 360, y = 66)

SetTemp_var     = tk.StringVar()
SetTemp_entry   = ttk.Entry(window, width = 15, textvariable = SetTemp_var, justify='center')
SetTemp_entry.bind("<Return>", SetTemponEnter)
SetTemp_entry.bind("<KP_Enter>", SetTemponEnter)
SetTemp_entry.grid(column = 0, row = 2)
setTempButton   = ttk.Button(window, text = "SET", command = SetTemp)
setTempButton.grid(column = 0, row = 3)

ttk.Button(window, text = "Options", command = OpenSettings).grid(column= 3, row = 0)

ports = serial.tools.list_ports.comports()
devices = []
for port in sorted(ports):
    devices.append(port.device)

if not devices: devices.append("N/A")

value_inside = tkinter.StringVar(window)
ChooseSerialMenu = OptionMenu(window, value_inside, *devices )
ChooseSerialMenu.grid(column= 0, row = 0)
setSerialButton = tkinter.Button(window, text = "Open", command = OpenSerial)
setSerialButton.grid(column= 1, row = 0)

animation = FuncAnimation(graph.figure, graph.update, interval=200)
animation.event_source.stop()

window.after(300, ReadCurrentTemp)
window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()