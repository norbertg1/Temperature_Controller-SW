from typing import Text
from tkinter import ttk
import tkinter as tk
from Settings import *
from Communication import serial_communication
import struct

window = tk.Tk()
 
window.title("Temperature Controller")
window.minsize(600,400)
serial_port = serial_communication()        #This is the constructor for serial_port class in Communication.py

def SetTemp():
    current_temp = SetTemp_var.get()
    
    #send on serial port out

def OpenSettings():
    settings = Settings_(serial_port)
    return None

def ReadCurrentTemp():
    current_temp = 999.999
    current_temp = serial_port.Read(4)
    try:
        serial_data = struct.unpack('f', current_temp)
        print(serial_data)
        print(current_temp)
    except:
        # I/O Error, add error handler
        serial_data = 0.0  
    #current_temp = current_temp.__round__(3)
    currentTemp_label.configure(text= str(serial_data) + " ℃")
    window.after(200, ReadCurrentTemp)
    return None

ttk.Label(window, text = "Enter Temperature").grid(column = 0, row = 0)
currentTemp_label = ttk.Label(window, text = None, font= ("default", "24", "bold") )
currentTemp_label.place(x = 150, y = 0)

SetTemp_var = tk.StringVar()
ttk.Entry(window, width = 15, textvariable = SetTemp_var).grid(column = 0, row = 1)
setTempButton = ttk.Button(window, text = "SET", command = SetTemp)
setTempButton.grid(column= 0, row = 2)

ttk.Button(window, text = "Options", command = OpenSettings).place(x= 400, y = 20)
i=0
window.after(300, ReadCurrentTemp)
window.mainloop()