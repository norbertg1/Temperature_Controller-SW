from cgitb import text
from genericpath import exists
from pyexpat import ErrorString
from time import sleep
from tkinter import *
import tkinter
from turtle import color
from Settings import *
from threading import Thread
import threading
import pyautogui

#from TempControl import SetTemp as SetTempp

class MeasureRange():
      def __init__(self, graph, settings, SetTemp_entry):
            self.graph              = graph
            self.settings           = settings
            self.SetTemp_entry      = SetTemp_entry
            self.stage              = -1
            self.temp               = 0
            self.OverallError       = 0
            self.error_str          = ""
            
      def OpenMeasureRange(self):
            self.SettingsWindow = tkinter.Tk()
            self.SettingsWindow.title("MeasureRange")
            self.SettingsWindow.minsize(350,250)
            FileStringVar = tkinter.StringVar(self.SettingsWindow,value='default text')
            StartTempVar = tkinter.StringVar(self.SettingsWindow,value='20')
            StepSizeVar = tkinter.StringVar(self.SettingsWindow,value='25')
            EndTempVar = tkinter.StringVar(self.SettingsWindow,value='100')
            MeasurementLengthVar = tkinter.StringVar(self.SettingsWindow,value='0.1')
            WaitBeforeMeasurementVar = tkinter.StringVar(self.SettingsWindow,value='0.1')
            
            self.status = tkinter.Label(self.SettingsWindow, text = "Not started", font= ("default", "10", "bold"))
            self.time_remaining = tkinter.Label(self.SettingsWindow, text = "", font= ("default", "10"))
            self.FileStringEntry = tkinter.Entry(self.SettingsWindow, width = 20, textvariable = FileStringVar)
            self.StartTempEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = StartTempVar)
            self.StepEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = StepSizeVar)
            self.EndTemptEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = EndTempVar)
            self.MeasureLengthEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = MeasurementLengthVar)
            self.WaitBeforeMeasurementEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = WaitBeforeMeasurementVar)
            self.StartStopButton   = tkinter.Button(self.SettingsWindow, text = "START", command = self.Start, width = 20)
            
            tkinter.Label(self.SettingsWindow, text = "Name of the file").place(x = 10, y = 0)
            tkinter.Label(self.SettingsWindow, text = "Start Temp.").place(x = 10, y = 50)
            tkinter.Label(self.SettingsWindow, text = "Step size").place(x = 130, y = 50)
            tkinter.Label(self.SettingsWindow, text = "End Temp.").place(x = 230, y = 50)
            tkinter.Label(self.SettingsWindow, text = "Measurement Length").place(x = 10, y = 120)
            tkinter.Label(self.SettingsWindow, text = "Wait Before measurement").place(x = 170, y = 120)
            tkinter.Label(self.SettingsWindow, text = "Status:").place(x = 10, y = 220)
            tkinter.Label(self.SettingsWindow, text = "°C").place(x =100, y = 70)
            tkinter.Label(self.SettingsWindow, text = "°C").place(x = 210, y = 70)
            tkinter.Label(self.SettingsWindow, text = "°C").place(x = 320, y = 70)
            tkinter.Label(self.SettingsWindow, text = "min.").place(x = 130, y = 140)
            tkinter.Label(self.SettingsWindow, text = "min.").place(x = 300, y = 140)
            tkinter.Button(self.SettingsWindow, text = "Next Step", command = self.NextStep, width = 10).place(x = 220, y = 180)
            
            self.status.place(x = 60, y = 220)
            self.time_remaining.place(x = 290, y = 220)
            self.FileStringEntry.place(x = 10, y = 20)
            self.StartTempEntry.place(x = 10, y = 70)
            self.StepEntry.place(x = 120, y = 70)
            self.EndTemptEntry.place(x = 230, y = 70)
            self.MeasureLengthEntry.place(x = 40, y = 140)
            self.WaitBeforeMeasurementEntry.place(x = 210, y = 140)
            self.StartStopButton.place(x = 20, y = 180)


      def SetTemp(self, value):
            self.SetTemp_entry.delete(0, END)
            self.SetTemp_entry.insert(0, round(int(value),3))
            self.graph.setTargetTempline(int(value))
            self.settings.data[Settings_.TargetTemp] = int(value*10)
            self.settings.data[Settings_.MenuNumber] = 1                    #Set menu to start heating or cooling
            if self.settings.SendSettings() is True: self.settings.DeviceStatus.status("Device OK", True)
            else: self.settings.DeviceStatus.status("Device Error", False)
            return None

      def Start(self):
            print("start")
            self.CurrentTargetTemp        = float(self.StartTempEntry.get())
            self.Step                     = float(self.StepEntry.get())
            self.EndTemp                  = float(self.EndTemptEntry.get())
            self.MeasurementLength        = float(self.MeasureLengthEntry.get())
            self.WaitBeforeMeasurement    = float(self.WaitBeforeMeasurementEntry.get())
            self.cnt                      = 0
            if self.stage == -1:    
                  self.stage = 0
                  self.StartStopButton.config(text = "STOP")
                  self.SettingsWindow.after(1000,self.ongoing_measurement)
            else: 
                  self.stage = -1
                  self.StartStopButton.config(text = "START")
                  
      def ongoing_measurement(self):
            if self.stage == 0: #Setting up the target temperature.
                  self.SetTemp(self.CurrentTargetTemp)
                  self.stage = 1
                  self.MaxTempDifference = 0
                  self.CurrentTargetError = 0
            if self.stage == 1: #Waiting before measurement.
                  self.status.configure(text= "Waiting before measurement", fg= "black")
                  self.time_remaining.configure(text= str(int(self.WaitBeforeMeasurement*60) - self.cnt) + " s") 
                  if self.cnt >= self.WaitBeforeMeasurement*60: 
                        self.ConfigIVMASTER()
                        self.cnt = 0
                        self.stage = 2
                  self.cnt += 1
                  self.SettingsWindow.after(1000,self.ongoing_measurement)
                  return
            if self.stage == 2: #Waiting for measuring.
                  if(abs(self.temp-self.CurrentTargetTemp) > 5): self.TargetTempError()
                  self.status.configure(text= "Measuring")
                  self.time_remaining.configure(text= str(int(self.MeasurementLength*60) - self.cnt) + " s")
                  if self.cnt >= self.MeasurementLength*60:
                        self.cnt = 0
                        self.stage = 3
                  self.cnt += 1
                  self.SettingsWindow.after(1000,self.ongoing_measurement)
                  return
            if self.stage == 3: #Finished, moving to next temperature or finishing
                  if self.CurrentTargetError == 1: self.error_str += self.currenterror_str
                  if self.CurrentTargetTemp == self.EndTemp: 
                        if(self.OverallError == 0): self.status.configure(text= "Finished", fg= "green")
                        else: self.status.configure(text= "Finished with errors", fg= "red")
                        self.time_remaining.configure(text= "")
                        self.stage = -1
                        if(self.OverallError == 1): self.ShowErrorWindow()
                        return
                  if self.CurrentTargetTemp < self.EndTemp: 
                        self.CurrentTargetTemp += self.Step
                        self.stage = 0
                  if self.CurrentTargetTemp > self.EndTemp:
                        self.CurrentTargetTemp = self.EndTemp
                        self.stage = 0
                  self.SettingsWindow.after(1000,self.ongoing_measurement)
      
      
      def ConfigIVMASTER(self):
            print("Range measurement. Configuring IVMASTER program")
            #pyautogui.click(300, 300)
            #pyautogui.moveTo(300, 300, 3)
            #pyautogui.click()
            #pyautogui.locateOnScreen('start.png')
            #pyautogui.click('calc7key.png')
            sleep(0.01)
            #pyautogui.write(self.FileStringEntry.get() + str(self.CurrentTargetTemp), interval=0.1)
            #pyautogui.press('Enter')
            #pyautogui.hotkey('alt', 'tab')
            
      def NextStep(self):
            if self.stage > -1 and self.stage < 3: 
                  self.stage += 1
                  self.cnt = 0

      def UpdateTemp(self, temp):
            self.temp = temp

      def TargetTempError(self):
            self.OverallError = 1
            self.CurrentTargetError = 1
            current_time = time.strftime("%H:%M:%S", time.localtime())
            if(abs(self.temp - self.CurrentTargetTemp) > self.MaxTempDifference): 
                  self.currenterror_str = current_time + " " + str(self.CurrentTargetTemp) + "°C  " + str(round(self.temp,2)) + "°C  Δ" + str(round(abs(self.temp - self.CurrentTargetTemp),2)) + "°C\n"
                  self.MaxTempDifference = abs(self.temp - self.CurrentTargetTemp)

      def ShowErrorWindow(self):
            ErrorWindow = tkinter.Tk()
            ErrorWindow.title("Errors")
            ErrorWindow.minsize(350,250)
            ErrorText = tkinter.Text(ErrorWindow, width = 60, height = 30)
            ErrorText.grid(column= 0, row = 0)
            ErrorText.insert(END, self.error_str)