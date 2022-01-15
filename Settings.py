from tkinter import *
import tkinter
import serial
import time
import struct
import crcmod
from help import ShowHelp
class Settings_():

   attempts    = 50

   CRC         = 0
   TargetTemp  = 1
   OffsetTemp  = 2
   MenuNumber  = 3
   maxP        = 15
   mode        = 6   
   sensor      = 7
   freq        = 8
   Kp          = 9
   Kd          = 10
   Ki          = 11
   filter      = 16

   def __init__(self, serial_port, window):
      self.serial_port = serial_port
      self.DeviceStatus    =  DeviceStat(window)
      self.TargetTemp_var  =  tkinter.StringVar()
      self.OffsetTemp_var  =  tkinter.StringVar()
      self.Menu_var        =  tkinter.StringVar()
      self.maxP_var        =  tkinter.StringVar()
      self.mode_var        =  tkinter.StringVar()
      self.sensor_var      =  tkinter.StringVar()
      self.freq_var        =  tkinter.StringVar()
      self.filter_var      =  tkinter.StringVar()
      self.Kp_var          =  tkinter.StringVar()
      self.Kd_var          =  tkinter.StringVar()
      self.Ki_var          =  tkinter.StringVar()

   def __del__(self):
      if 'self.SettingsWindow' in locals(): self.SettingsWindow.destroy()
      print("Destructor called")
    
   def OpenSettingsWindow(self):
      
      self.SettingsWindow = tkinter.Tk()
      self.SettingsWindow.title("Settings")
      self.SettingsWindow.minsize(300,200)
      self.SettingsWindow.resizable(False, False)
      
      tkinter.Button(self.SettingsWindow, text = "Read Settings", command = self.ReadSettings).grid(column= 0, row = 0)
      tkinter.Button(self.SettingsWindow, text = "Write Settings", command = self.GetandSendSettings).grid(column= 1, row = 0)
      tkinter.Button(self.SettingsWindow, text = "Reset Device", command = self.ResetDevice).grid(column= 2, row = 0)
      tkinter.Button(self.SettingsWindow, text = "Load  Defaults", command = self.LoadDefaults).grid(column= 3, row = 0)
      tkinter.Button(self.SettingsWindow, text = "Help", command = self.Help).grid(column= 2, row = 7)


      tkinter.Label(self.SettingsWindow, text = "Offset Temp").grid(column = 0, row = 2)
      tkinter.Label(self.SettingsWindow, text = "Menu").grid(column = 0, row = 3)
      tkinter.Label(self.SettingsWindow, text = "Max. Power").grid(column = 0, row = 4)
      tkinter.Label(self.SettingsWindow, text = "Mode").grid(column = 0, row = 5)
      tkinter.Label(self.SettingsWindow, text = "Sensor").grid(column = 0, row = 6)
      tkinter.Label(self.SettingsWindow, text = "Freq.").grid(column = 0, row = 7)
      tkinter.Label(self.SettingsWindow, text = "  Kp").grid(column = 2, row = 2)
      tkinter.Label(self.SettingsWindow, text = "  Kd").grid(column = 2, row = 3)
      tkinter.Label(self.SettingsWindow, text = "  Ki").grid(column = 2, row = 4)
      tkinter.Label(self.SettingsWindow, text = "Temp. filter").grid(column = 2, row = 5)

      self.OffsetTemp_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.OffsetTemp_var)
      self.Menu_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.Menu_var)
      self.maxP_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.maxP_var)
      self.Mode_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.mode_var)
      self.Sensor_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.sensor_var)
      self.Freq_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.freq_var)
      self.Kp_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.Kp_var)
      self.Kd_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.Kd_var)
      self.Ki_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.Ki_var)
      self.Filter_entry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = self.filter_var)

      self.OffsetTemp_entry.grid(column = 1, row = 2)
      self.Menu_entry.grid(column = 1, row = 3)
      self.maxP_entry.grid(column = 1, row = 4)
      self.Mode_entry.grid(column = 1, row = 5)
      self.Sensor_entry.grid(column = 1, row = 6)      
      self.Freq_entry.grid(column = 1, row = 7)
      self.Kp_entry.grid(column = 3, row = 2)
      self.Kd_entry.grid(column = 3, row = 3)
      self.Ki_entry.grid(column = 3, row = 4)
      self.Filter_entry.grid(column = 3, row = 5)
      self.RefreshTextSettings()      
      self.SettingsWindow.mainloop()
   
   def ReadSettings(self):
      self.serial_port.flushCache()
      self.serial_port.Write_unicode("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
      time.sleep(0.01)
      settings_raw = self.serial_port.Read(64)
      i=0
      while(1):       
         try:
            i+=1
            print("received raw data:", settings_raw.hex())  
            crc32 = crcmod.predefined.mkCrcFun('crc-32-mpeg')(settings_raw[4:64])
            self.data = struct.unpack('Iiihhhiiiiiifffif', settings_raw)
            self.data = list(self.data)
            print("received data:", self.data)
            if crc32 == self.data[self.CRC]:
               print("UART received CRC is ok!")
               return TRUE
            raise Exception()
         except:
            if i>self.attempts: break
            self.serial_port.flushCache()
            self.serial_port.Write_unicode("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            time.sleep(0.01)
            settings_raw = self.serial_port.Read(64)  
            time.sleep(0.1)
      return FALSE

   def RefreshTextSettings(self):
      #print(str(self.data[0]))
      self.TargetTemp_var = self.data[self.TargetTemp]
      self.OffsetTemp_entry.delete(0, END)
      self.OffsetTemp_entry.insert(0, self.data[self.OffsetTemp])
      self.Menu_entry.delete(0, END)
      self.Menu_entry.insert(0, self.data[self.MenuNumber])
      self.maxP_entry.delete(0, END)
      self.maxP_entry.insert(0, self.data[self.maxP])
      self.Mode_entry.delete(0, END)
      self.Mode_entry.insert(0, self.data[self.mode])
      self.Sensor_entry.delete(0, END)
      self.Sensor_entry.insert(0, self.data[self.sensor])      
      self.Freq_entry.delete(0, END)
      self.Freq_entry.insert(0, self.data[self.freq])
      self.Filter_entry.delete(0, END)
      self.Filter_entry.insert(0, round(self.data[self.filter],2))
      self.Kp_entry.delete(0, END)
      self.Kp_entry.insert(0, self.data[self.Kp])
      self.Kd_entry.delete(0, END)
      self.Kd_entry.insert(0, self.data[self.Kd])
      self.Ki_entry.delete(0, END)
      self.Ki_entry.insert(0, self.data[self.Ki])

   def GetandSendSettings(self):
      self.data[self.TargetTemp] = self.TargetTemp_var
      self.data[self.OffsetTemp] = int(self.OffsetTemp_entry.get())*10
      self.data[self.MenuNumber] = int(self.Menu_entry.get())
      self.data[self.maxP] = int(self.maxP_entry.get())
      self.data[self.mode] = int(self.Mode_entry.get())
      self.data[self.sensor] = int(self.Sensor_entry.get())
      self.data[self.freq] = int(self.Freq_entry.get())
      self.data[self.filter] = float(self.Filter_entry.get())
      self.data[self.Kp] = int(self.Kp_entry.get())
      self.data[self.Kd] = int(self.Kd_entry.get())
      self.data[self.Ki] = int(self.Ki_entry.get())
      if self.SendSettings() is True:  self.DeviceStatus.status("Device OK", True)
      else: self.DeviceStatus.status("Device Error", False)

   def SendSettings(self):
      try:
         settings_tuple = tuple(self.data)
         settings_raw = struct.pack("iihhhiiiiiifffif", *settings_tuple[1:17])
         crc32 = crcmod.predefined.mkCrcFun('crc-32-mpeg')(settings_raw)
         settings_raw = struct.pack("Iiihhhiiiiiifffif", crc32, *settings_tuple[1:17])
         print("Settings going to send:", settings_tuple)
         print("Settings going to send (raw):", settings_raw.hex())
         print("Settings going CRC checksum:", crc32)
         if self.WritToDevice(settings_raw) is True:
            print("Settings saved to device OK!")
            return True
         else: 
            return False
      except Exception as e: 
         print(settings_tuple)
         print(e)
         return False

   def ResetDevice(self):
      print("Resetting Device")
      if self.WritToDevice("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR".encode()) is True:
         print("Device reset completed")
         self.DeviceStatus.status("Device OK", True)
      else:
         print("Device reset error")
         self.DeviceStatus.status(False)
         self.DeviceStatus.status("No Answer", False)

   def LoadDefaults(self):
      print("Load defaults values into device")
      if self.WritToDevice("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD".encode()) is True:
         print("Device set to defaults")
         self.DeviceStatus.status("Device OK", True)
      else:
         print("Device set to defaults error")
         self.DeviceStatus.status("No Answer", False)

   def WritToDevice(self, message):
      self.serial_port.flushCache()
      self.serial_port.Write(message)
      i=0
      while(1):
         try:
            i+=1
            if i>self.attempts: break
            print("Tries:", i)
            self.serial_port.flushCache()
            raw = self.serial_port.Read(4)
            txt = struct.unpack("cccc", raw)
            print("Answer:", txt, "in hex:", raw.hex())
            if txt[0] == b'O' and txt[1] == b'O' and txt[2] == b'O' and txt[3] == b'O':
               return True
            else: raise Exception() 
         except:
            self.serial_port.flushCache()
            self.serial_port.Write(message)
            #time.sleep(0.005)
      time.sleep(0.5)
      self.serial_port.flushCache()
      return False

   def Quit(self):
      Settings_.dest

   def Help(self):
      self.HelpWindow = tkinter.Tk()
      self.SettingsWindow.title("Settings")
      self.SettingsWindow.minsize(300,200)
      ShowHelp(self.HelpWindow)
class DeviceStat():
   def __init__(self, window):
      self.CurrentStatus = False
      self.DeviceStatus_label = tkinter.Label(window)
      self.DeviceStatus_label.grid(column= 6, row = 0)

   def status(self, message, stat):
      self.CurrentStatus = stat
      if(stat is False):   self.DeviceStatus_label.config(text = " " + message, font= ("default", "12", "bold"), fg="red")
      if(stat is True):    self.DeviceStatus_label.config(text = " " + message, font= ("default", "12", "bold"), fg="green")

   def GetStatus(self):
      return self.CurrentStatus