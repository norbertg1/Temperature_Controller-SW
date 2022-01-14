from time import sleep
from tkinter import *
import tkinter
from turtle import color
from Settings import *
from threading import Thread
import threading

#from TempControl import SetTemp as SetTempp

class MeasureRange():
      def __init__(self, graph, settings, SetTemp_entry):
            self.graph              = graph
            self.settings           = settings
            self.SetTemp_entry      = SetTemp_entry
            self.nextstep           = 0
            self.th = threading.Thread(target=self.start_thread)
            
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
            
            self.status.place(x = 60, y = 220)
            self.time_remaining.place(x = 290, y = 220)
            self.FileStringEntry.place(x = 10, y = 20)
            self.StartTempEntry.place(x = 10, y = 70)
            self.StepEntry.place(x = 120, y = 70)
            self.EndTemptEntry.place(x = 230, y = 70)
            self.MeasureLengthEntry.place(x = 40, y = 140)
            self.WaitBeforeMeasurementEntry.place(x = 210, y = 140)
            
            StartButton   = tkinter.Button(self.SettingsWindow, text = "START", command = self.Start, width = 20).place(x = 20, y = 180)
            NextStepButton   = tkinter.Button(self.SettingsWindow, text = "Next Step", command = self.NextStep, width = 10).place(x = 220, y = 180)


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
            #self.th.start()
            print("start")
            self.CurrentTargetTemp        = float(self.StartTempEntry.get())
            self.Step                     = float(self.StepEntry.get())
            self.EndTemp                  = float(self.EndTemptEntry.get())
            self.MeasurementLength        = float(self.MeasureLengthEntry.get())
            self.WaitBeforeMeasurement    = float(self.WaitBeforeMeasurementEntry.get())
            self.stage                    = 0
            self.cnt                      = 0
            self.SettingsWindow.rgbafter(1000,self.ongoing_measurement)
      
      def ongoing_measurement(self):
            print(".")
            if self.stage == 0:
                  print("Range measurement. Setting up the target temperature.")
                  self.SetTemp(self.CurrentTargetTemp)
                  self.stage = 1
            if self.stage == 1:
                  print("Range measurement. Waiting before measurement.")
                  self.status.configure(text= "Waiting before measurement", fg= "black")
                  self.time_remaining.configure(text= str(self.WaitBeforeMeasurement*60 - self.cnt) + " s") 
                  if self.cnt >= self.WaitBeforeMeasurement*60: 
                        self.cnt = 0
                        self.stage = 2
                  print(self.cnt)
                  self.cnt += 1
                  self.SettingsWindow.after(1000,self.ongoing_measurement)
                  return
            if self.stage == 2:
                  print("Range measurement. Measuring.")
                  self.status.configure(text= "Measuring")
                  self.time_remaining.configure(text= str(self.MeasurementLength*60 - self.cnt) + " s")
                  #self.ConfigIVMASTER()
                  if self.cnt >= self.MeasurementLength*60:
                        self.cnt = 0
                        self.stage = 3
                  self.cnt += 1
                  self.SettingsWindow.after(1000,self.ongoing_measurement)
                  return
            if self.stage == 3:
                  if self.CurrentTargetTemp == self.EndTemp: 
                        print("Range measurement. Finished.")
                        self.status.configure(text= "Finished", fg= "green")
                  if self.CurrentTargetTemp > self.EndTemp: 
                        self.CurrentTargetTemp = self.EndTemp
                        self.stage = 0
                        self.SettingsWindow.after(1000,self.ongoing_measurement)
                  if self.CurrentTargetTemp < self.EndTemp: 
                        self.CurrentTargetTemp += self.Step
                        self.stage = 0
                        self.SettingsWindow.after(1000,self.ongoing_measurement)
      
      def start_thread(self):
            print("Starting range measurement")
            self.status.configure(text= "Waiting before measurement")
            #StartTemp               = int(self.StartTempEntry.get())
            #Step                    = int(self.StepEntry.get())
            #EndTemp                 = int(self.EndTemptEntry.get())
            #MeasurementLength       = int(self.MeasureLengthEntry.get())
            #WaitBeforeMeasurement   = int(self.WaitBeforeMeasurementEntry.get())
            
            StartTemp               = 1
            Step                    = 2
            EndTemp                 = 10
            MeasurementLength       = 1
            WaitBeforeMeasurement   = 1
            
            print("debug")
            CurrentTargetTemp = StartTemp
            while CurrentTargetTemp < EndTemp:
                  print("Range measurement. Setting up the target temperature.")
                  self.SetTemp(CurrentTargetTemp)
                  print("Range measurement. Waiting before measurement.")
                  self.status.configure(text= "Waiting before measurement")
                  self.sleep(int(WaitBeforeMeasurement)*60)
                  print("Range measurement. Measuring.")
                  self.status.configure(text= "Measuring")
                  self.ConfigIVMASTER()
                  self.sleep(int(MeasurementLength)*60)
                  CurrentTargetTemp += Step
                  if CurrentTargetTemp == EndTemp: 
                        print("Range measurement. Finished.")
                        self.status.configure(text= "Finished", fg= "green")
                        break
                  if CurrentTargetTemp > EndTemp: CurrentTargetTemp = EndTemp
                  
      
      
      def sleep(self, value):
            print("sleep")
            for i in range(value, 0, -1):
                  print(i)
                  self.time_remaining.configure(text= str(i) + " s")
                  #event.wait(1)
                  sleep(1)
                  if self.nextstep == 1:
                        self.nextstep=0
                        break
      
      def ConfigIVMASTER(self):
            print("Range measurement. Configuring IVMASTER program")
            
      def NextStep(self):
            self.nextstep=1            

class first(Thread):
      def one_sec(self):
            sleep(1)
            print("sleep")