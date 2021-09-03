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
      
      self.TargetTemp_var=tkinter.StringVar()
      self.OffsetTemp_var=tkinter.StringVar()
      self.Menu_var=tkinter.StringVar()
      
   def OpenSettingsWindow(self):
      
      self.SettingsWindow = tkinter.Tk()
      self.SettingsWindow.title("Settings")
      self.SettingsWindow.minsize(300,200)

      tkinter.Button(self.SettingsWindow, text = "Read Settings", command = self.ReadSettings).grid(column= 0, row = 0)
      tkinter.Button(self.SettingsWindow, text = "Write Settings", command = self.GetandSendSettings).grid(column= 1, row = 0)
      
      tkinter.Label(self.SettingsWindow, text = "Offset Temp").grid(column = 0, row = 2)
      tkinter.Label(self.SettingsWindow, text = "Menu").grid(column = 0, row = 3)

      self.OffsetTemp_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.OffsetTemp_var)
      self.Menu_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.Menu_var)

      self.OffsetTemp_entry.grid(column = 1, row = 2)
      self.Menu_entry.grid(column = 1, row = 3)
      self.RefreshTextSettings()      
      self.SettingsWindow.mainloop()
   
   def ReadSettings(self):
      tries = 0
      while tries<10:
         tries+=1
         self.serial_port.flushCache()
         self.serial_port.Write_unicode("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
         time.sleep(0.01)
         settings_raw = self.serial_port.Read(64)
         i=0
         while(1):       
            try:
               i+=1
               print("received raw data:", settings_raw.hex())  
               crc32 = crcmod.predefined.mkCrcFun('crc-32-mpeg')(settings_raw[0:60])
               self.data = struct.unpack('iihhhiiiiiifffifI', settings_raw)
               break
            except:
               if i>20: break
               self.serial_port.flushCache()
               self.serial_port.Write_unicode("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
               time.sleep(0.01)
               settings_raw = self.serial_port.Read(64)
         self.data = list(self.data)
         print("received data:", self.data)  
         if crc32 == self.data[16]:
            print("UART received CRC is ok!")
            return TRUE
         time.sleep(0.1)
      return FALSE

   def RefreshTextSettings(self):
      print(str(self.data[0]))
      self.TargetTemp_var = self.data[0]
      self.OffsetTemp_entry.delete(0, END)
      self.OffsetTemp_entry.insert(0, self.data[1])
      self.Menu_entry.delete(0, END)
      self.Menu_entry.insert(0, self.data[2])

   def GetandSendSettings(self):
      self.data[0] = int(self.TargetTemp_var)
      print(self.OffsetTemp_var.get())
      self.data[1] = int(self.OffsetTemp_var.get())
      self.data[2] = int(self.Menu_var.get())
      self.SendSettings()

   def SendSettings(self):
      settings_tuple = tuple(self.data)
      settings_raw = struct.pack("iihhhiiiiiifffif", *settings_tuple[0:16])
      crc32 = crcmod.predefined.mkCrcFun('crc-32-mpeg')(settings_raw)
      settings_raw = struct.pack("iihhhiiiiiifffifI", *settings_tuple[0:16], crc32)
      print("Settings going to send:", settings_tuple)
      print("Settings going to send (raw):", settings_raw.hex())
      i=0
      while(1):
         try:
            i+=1
            if i>20: break
            print("Tries:", i)
            self.serial_port.flushCache()
            raw = self.serial_port.Read(4)
            txt = struct.unpack("cccc", raw)
            print("Answer:", txt, "in hex:", raw.hex())
            if txt[0] == b'O' and txt[1] == b'O' and txt[2] == b'O' and txt[3] == b'O':
                print("Settings saved in device!")
                break
            else: raise Exception() 
         except:
            print("fdsfd")
            self.serial_port.flushCache()
            self.serial_port.Write(settings_raw)
            time.sleep(0.01)

      time.sleep(0.5)
      self.serial_port.flushCache()