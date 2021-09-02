from tkinter import *
import tkinter
import serial.tools.list_ports
import serial
import time
import struct
import crcmod

class Settings_():
   def __init__(self, serial_port):
      self.serial_port = serial_port
      self.SettingsWindow = tkinter.Tk()
      self.SettingsWindow.title("Settings")
      self.SettingsWindow.minsize(300,200)
      
      tkinter.Button(self.SettingsWindow, text = "Read Settings", command = self.ReadSettings).grid(column= 0, row = 0)
      tkinter.Button(self.SettingsWindow, text = "Write Settings", command = self.WriteSettings).grid(column= 1, row = 0)
      
      self.TargetTemp_var=tkinter.StringVar()
      self.OffsetTemp_var=tkinter.StringVar()
      self.Menu_var=tkinter.StringVar()
      
      tkinter.Label(self.SettingsWindow, text = "Offset Temp").grid(column = 0, row = 2)
      tkinter.Label(self.SettingsWindow, text = "Menu").grid(column = 0, row = 3)

      self.OffsetTemp_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.OffsetTemp_var)
      self.Menu_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.Menu_var)

      self.OffsetTemp_entry.grid(column = 1, row = 2)
      self.Menu_entry.grid(column = 1, row = 3)
      
      
      self.SettingsWindow.mainloop()
   
   def ReadSettings(self):
      tries = 0
      while tries<10:
         tries+=1
         self.serial_port.flusCache()
         self.serial_port.Write("SSSSSSSSSSSSSSSSS")
         settings_raw = self.serial_port.Read(64)
         print(settings_raw.hex())  
         crc32 = crcmod.predefined.mkCrcFun('crc-32-mpeg')(settings_raw[0:60])
         self.settings = struct.unpack('iiihhhiiiiifffifI', settings_raw)
         if crc32 == self.settings[16]:
            print("UART received CRC is ok!")
            self.RefreshTextSettings()
            break
         time.sleep(0.1)

   def RefreshTextSettings(self):
      print(str(self.settings[0]))
      self.TargetTemp_var = self.settings[0]
      self.OffsetTemp_entry.delete(0, END)
      self.OffsetTemp_entry.insert(0, self.settings[1])
      self.Menu_entry.delete(0, END)
      self.Menu_entry.insert(0, self.settings[2])

   def WriteSettings(self):
      self.settings[0] = self.TargetTemp_var
      self.settings[1] = self.OffsetTemp_var.get()
      self.settings[2] = self.Menu_var.get()
      print(settings)
      self.serial_port.Write("0")