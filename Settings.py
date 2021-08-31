from tkinter import *
import tkinter
import serial.tools.list_ports
import serial
import time

class Settings_():
   def __init__(self, serial_port):
      self.serial_port = serial_port
      ports = serial.tools.list_ports.comports()
      self.SettingsWindow = tkinter.Tk()
      self.SettingsWindow.title("Settings")
      self.SettingsWindow.minsize(300,200)
      self.value_inside = tkinter.StringVar(self.SettingsWindow)
      devices = []
      for port in sorted(ports):
        devices.append(port.device)
      self.ChooseSerialMenu = OptionMenu(self.SettingsWindow, self.value_inside ,*devices )
      self.ChooseSerialMenu.grid(column= 1, row = 0)
      self.setSerialButton = tkinter.Button(self.SettingsWindow, text = "Open", command = self.OpenSerial)
      self.setSerialButton.grid(column= 2, row = 0)
      tkinter.Button(self.SettingsWindow, text = "Read Settings", command = self.ReadSettings).grid(column= 4, row = 0)
      tkinter.Button(self.SettingsWindow, text = "Write Settings", command = self.WriteSettings).grid(column= 5, row = 0)
      self.SettingsWindow.mainloop()

   def OpenSerial(self):
      print("Selected Option: {}".format(self.value_inside.get()))
      if(self.serial_port.Open(self.value_inside.get())):
         tkinter.Label(self.SettingsWindow, text = "Ok", font= ("default", "12", "bold")).grid(column= 3, row = 0)
      else:
         tkinter.Label(self.SettingsWindow, text = "Failed", font= ("default", "12", "bold")).grid(column= 3, row = 0)
      return None

   def ReadSettings(self):
      self.serial_port.Write("S")
      time.sleep(10)
      data = 0
      self.serial_port.Read(data, 30)

   def WriteSettings(self):
      self.serial_port.Write("0")