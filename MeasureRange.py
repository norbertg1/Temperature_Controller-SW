from cgitb import text
from genericpath import exists
from pyexpat import ErrorString
from time import sleep
import tkinter
from turtle import color
from Settings import *
import pyautogui
import WhereToClick_Buttons
import base64
from io import BytesIO
from PIL import Image, ImageQt

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
            self.MeasureRangeWindow = Toplevel()
            self.MeasureRangeWindow.title("MeasureRange")
            self.MeasureRangeWindow.minsize(370,280)
            self.MeasureRangeWindow.resizable(False, False)
            FileStringVar = tkinter.StringVar(self.MeasureRangeWindow,value='default text')
            StartTempVar = tkinter.StringVar(self.MeasureRangeWindow,value='20')
            StepSizeVar = tkinter.StringVar(self.MeasureRangeWindow,value='25')
            EndTempVar = tkinter.StringVar(self.MeasureRangeWindow,value='100')
            MeasurementLengthVar = tkinter.StringVar(self.MeasureRangeWindow,value='20')
            WaitBeforeMeasurementVar = tkinter.StringVar(self.MeasureRangeWindow,value='20')
            self.ControlIVMasterVar = tkinter.IntVar(value=0)
            self.ControlSpectLabVar = tkinter.IntVar(value=0)
            self.ControlPX5Var = tkinter.IntVar(value=0)

            self.status = tkinter.Label(self.MeasureRangeWindow, text = "Not started", font= ("default", "10", "bold"))
            self.time_remaining = tkinter.Label(self.MeasureRangeWindow, text = "", font= ("default", "10"))
            self.FileStringEntry = tkinter.Entry(self.MeasureRangeWindow, width = 24, textvariable = FileStringVar)
            self.StartTempEntry = tkinter.Entry(self.MeasureRangeWindow, width = 10, textvariable = StartTempVar)
            self.StepEntry = tkinter.Entry(self.MeasureRangeWindow, width = 10, textvariable = StepSizeVar)
            self.EndTemptEntry = tkinter.Entry(self.MeasureRangeWindow, width = 10, textvariable = EndTempVar)
            self.MeasureLengthEntry = tkinter.Entry(self.MeasureRangeWindow, width = 10, textvariable = MeasurementLengthVar)
            self.WaitBeforeMeasurementEntry = tkinter.Entry(self.MeasureRangeWindow, width = 10, textvariable = WaitBeforeMeasurementVar)
            self.StartStopButton   = tkinter.Button(self.MeasureRangeWindow, text = "START", command = self.Start, width = 20)
            self.ControlIVMasterButton = tkinter.Checkbutton(self.MeasureRangeWindow, variable=self.ControlIVMasterVar,text="Control IVMaster")
            self.ControlSpectLabButton = tkinter.Checkbutton(self.MeasureRangeWindow, variable=self.ControlSpectLabVar,text="Control SpectLab")
            self.ControlPX5 = tkinter.Checkbutton(self.MeasureRangeWindow, variable=self.ControlPX5Var,text="Control Amptek PX5")
            
            tkinter.Label(self.MeasureRangeWindow, text = "Name of the file").place(x = 10, y = 0)
            tkinter.Label(self.MeasureRangeWindow, text = "Start Temp.").place(x = 10, y = 65)
            tkinter.Label(self.MeasureRangeWindow, text = "Step size").place(x = 140, y = 65)
            tkinter.Label(self.MeasureRangeWindow, text = "End Temp.").place(x = 240, y = 65)
            tkinter.Label(self.MeasureRangeWindow, text = "Measurement Length").place(x = 10, y = 135)
            tkinter.Label(self.MeasureRangeWindow, text = "Wait Before measurement").place(x = 170, y = 135)
            tkinter.Label(self.MeasureRangeWindow, text = "Status:").place(x = 10, y = 250)
            tkinter.Label(self.MeasureRangeWindow, text = "°C").place(x =100, y = 90)
            tkinter.Label(self.MeasureRangeWindow, text = "°C").place(x = 220, y = 90)
            tkinter.Label(self.MeasureRangeWindow, text = "°C").place(x = 330, y = 90)
            tkinter.Label(self.MeasureRangeWindow, text = "min.").place(x = 130, y = 160)
            tkinter.Label(self.MeasureRangeWindow, text = "min.").place(x = 300, y = 160)
            tkinter.Button(self.MeasureRangeWindow, text = "Next Step", command = self.NextStep, width = 10).place(x = 220, y = 210)
            
            self.ControlIVMasterButton.place(x = 210, y = 0)
            self.ControlSpectLabButton.place(x = 210, y = 20)
            self.ControlPX5.place(x = 210, y = 40)
            self.status.place(x = 60, y = 250)
            self.time_remaining.place(x = 290, y = 250)
            self.FileStringEntry.place(x = 10, y = 25)
            self.StartTempEntry.place(x = 10, y = 90)
            self.StepEntry.place(x = 130, y = 90)
            self.EndTemptEntry.place(x = 240, y = 90)
            self.MeasureLengthEntry.place(x = 40, y = 160)
            self.WaitBeforeMeasurementEntry.place(x = 210, y = 160)
            self.StartStopButton.place(x = 20, y = 210)


      def SetTemp(self, value):
            self.SetTemp_entry.delete(0, END)
            self.SetTemp_entry.insert(0, round(int(value),3))
            self.graph.setTargetTempline(int(value))
            self.settings.data[Settings_.TargetTemp] = int(value*10)
            self.settings.data[Settings_.MenuNumber] = 1                    #Set menu to start heating or cooling
            if self.settings.SendSettings() is True: self.settings.DeviceStatus.status("Device OK", True)
            else: self.settings.DeviceStatus.status("Device Error", False)
            return None

      def get_values_from_text_box(self):
            self.Step                     = float(self.StepEntry.get())
            self.EndTemp                  = float(self.EndTemptEntry.get())
            self.MeasurementLength        = float(self.MeasureLengthEntry.get())
            self.WaitBeforeMeasurement    = float(self.WaitBeforeMeasurementEntry.get())          
      
      def Start(self):
            print("start")
            self.get_values_from_text_box()
            self.CurrentTargetTemp        = float(self.StartTempEntry.get())
            self.cnt                      = 0
            if self.CurrentTargetTemp > self.EndTemp and self.Step > 0:
                  self.status.configure(text= "Range setting error", fg= "red")
                  return
            if self.CurrentTargetTemp < self.EndTemp and self.Step < 0:
                  self.status.configure(text= "Range setting error", fg= "red")
                  return
            if self.stage == -1:    
                  self.stage = 0
                  self.StartStopButton.config(text = "STOP")
                  self.MeasureRangeWindow.after(1000,self.ongoing_measurement)
            else: 
                  self.stage = -1
                  self.StartStopButton.config(text = "START")
                  self.status.configure(text= "Stopped", fg= "black")
                  
      def ongoing_measurement(self):
            if self.stage == 0: #Setting up the target temperature.
                  self.get_values_from_text_box()
                  self.SetTemp(self.CurrentTargetTemp)
                  self.stage = 1
                  self.MaxTempDifference = 0
                  self.CurrentTargetError = 0
            if self.stage == 1: #Waiting before measurement.
                  self.get_values_from_text_box()
                  self.status.configure(text= "Waiting before measurement", fg= "black")
                  self.time_remaining.configure(text= str(int(self.WaitBeforeMeasurement*60) - self.cnt) + " s") 
                  if self.cnt >= self.WaitBeforeMeasurement*60: 
                        self.ConfigIVMASTER()
                        self.ConfigSpectLab1()
                        self.ConfigPX5_1()
                        self.cnt = 0
                        self.stage = 2
                  self.cnt += 1
                  self.MeasureRangeWindow.after(1000,self.ongoing_measurement)
                  return
            if self.stage == 2: #Waiting for measuring.
                  self.get_values_from_text_box()
                  self.TargetTempError()
                  self.status.configure(text= "Measuring")
                  self.time_remaining.configure(text= str(int(self.MeasurementLength*60) - self.cnt) + " s")
                  if self.cnt >= self.MeasurementLength*60:
                        self.ConfigSpectLab2()
                        self.ConfigPX5_2()
                        self.cnt = 0
                        self.stage = 3
                        self.MeasureRangeWindow.after(10,self.ongoing_measurement)
                        return
                  self.cnt += 1
                  self.MeasureRangeWindow.after(1000,self.ongoing_measurement)
                  return
            if self.stage == 3: #Finished, moving to next temperature or finishing
                  self.get_values_from_text_box()
                  if self.CurrentTargetError == 1: self.error_str += self.currenterror_str
                  if self.CurrentTargetTemp == self.EndTemp: 
                        if(self.OverallError == 0): self.status.configure(text= "Finished", fg= "green")
                        else: self.status.configure(text= "Finished with errors", fg= "red")
                        self.StartStopButton.config(text = "START")
                        self.time_remaining.configure(text= "")
                        self.stage = -1
                        self.ShowErrorWindow()
                        return
                  if abs(self.CurrentTargetTemp) < abs(self.EndTemp): 
                        self.CurrentTargetTemp += self.Step
                        self.stage = 0
                  if abs(self.CurrentTargetTemp) > abs(self.EndTemp):
                        self.CurrentTargetTemp = self.EndTemp
                        self.stage = 0
                  self.MeasureRangeWindow.after(1000,self.ongoing_measurement)
      
      

      
      def CheckIVMasterCheckBox(self):
            return self.ControlIVMasterVar.get()
            
      def CheckSpectLabCheckBox(self):
            return self.ControlSpectLabVar.get()
      
      def CheckSpectPX5CheckBox(self):
            return self.ControlPX5Var.get()
      
      def ConfigPX5_1(self):
            if self.CheckSpectPX5CheckBox() == 1:
                  print("Range measurement. Starting Amptek PX5 measurement.")
                  ## Clicking on Amptek PX5 Erase button ##
                  PX5_Erase         = Image.open(BytesIO(base64.b64decode(WhereToClick_Buttons.PX5_Erase)))
                  location          = pyautogui.locateCenterOnScreen(PX5_Erase, grayscale=True, confidence=0.8)
                  if self.location_error(location) == 1: return
                  pyautogui.moveTo(location.x, location.y, 1)
                  pyautogui.click()
                  ## Clicking on Amptek PX5 Start button ##
                  PX5_Start         = Image.open(BytesIO(base64.b64decode(WhereToClick_Buttons.PX5_Start)))
                  location          = pyautogui.locateCenterOnScreen(PX5_Start, grayscale=True, confidence=0.8)
                  if self.location_error(location) == 1: return
                  pyautogui.moveTo(location.x, location.y, 1)
                  pyautogui.click()

      def ConfigPX5_2(self):
            if self.CheckSpectPX5CheckBox() == 1:
                  print("Range measurement. Saving Amptek PX5 measurement.")
                  ## Clicking on Amptek PX5 Stop button ##
                  PX5_Stop         = Image.open(BytesIO(base64.b64decode(WhereToClick_Buttons.PX5_Stop)))
                  location          = pyautogui.locateCenterOnScreen(PX5_Stop, grayscale=True, confidence=0.8)
                  if self.location_error(location) == 1: return
                  pyautogui.moveTo(location.x, location.y, 1)
                  pyautogui.click()
                  ## Clicking on Amptek PX5 Save button ##
                  PX5_Save      = Image.open(BytesIO(base64.b64decode(WhereToClick_Buttons.PX5_Save)))
                  location          = pyautogui.locateCenterOnScreen(PX5_Save, grayscale=True, confidence=0.8)
                  if self.location_error(location) == 1: return
                  pyautogui.moveTo(location.x, location.y, 1)
                  pyautogui.click()
                  sleep(1)
                  ## Writing file name ##
                  pyautogui.write(self.FileStringEntry.get() + str(int(self.CurrentTargetTemp)) + "C.mca", interval=0.1)
                  sleep(1)
                  pyautogui.press('Enter')
                  
      def ConfigIVMASTER(self):
            if self.CheckIVMasterCheckBox() == 1:
                  print("Range measurement. Starting IVMaster measurement.")
                  byte_data = base64.b64decode(WhereToClick_Buttons.IVMaster_start)
                  image_data = BytesIO(byte_data)
                  image = Image.open(image_data)
                  location = pyautogui.locateCenterOnScreen(image, grayscale=True, confidence=0.7)
                  #location = pyautogui.locateCenterOnScreen("image.png", grayscale=True, confidence=0.7)
                  if location is None: 
                        current_time = time.strftime("%H:%M:%S", time.localtime())
                        self.error_str += current_time + " " + str(self.CurrentTargetTemp) + " IVMaster start button location is not found.\n"
                        print ("IVMaster start button location is not found.")
                        self.OverallError = 1
                        return
                  pyautogui.moveTo(location.x, location.y, 3)
                  pyautogui.click()
                  pyautogui.write(self.FileStringEntry.get() + str(int(self.CurrentTargetTemp)) + "C.txt", interval=0.1)
                  pyautogui.press('Enter')
                  pyautogui.hotkey('alt', 'tab')
                  pyautogui.hotkey('alt', 'tab')
      
      def ConfigSpectLab1(self):
            if self.CheckSpectLabCheckBox() == 1:
                  print("Range measurement. Starting SpectLab measurement.")
                  ## Clicking on SpectLab_new ##
                  SpectLab_new      = Image.open(BytesIO(base64.b64decode(WhereToClick_Buttons.SpectLab_new)))
                  location          = pyautogui.locateCenterOnScreen(SpectLab_new, grayscale=True, confidence=0.7)
                  if self.location_error(location) == 1: return
                  pyautogui.moveTo(location.x, location.y, 3)
                  pyautogui.click()
                  ## Clicking on SpectLab_connect ##
                  SpectLab_Connect  = Image.open(BytesIO(base64.b64decode(WhereToClick_Buttons.SpectLab_connect)))
                  location          = pyautogui.locateCenterOnScreen(SpectLab_Connect, grayscale=True, confidence=0.7)
                  if self.location_error(location) == 1: return
                  pyautogui.moveTo(location.x, location.y, 1)
                  pyautogui.click()
                  sleep(1)
                  pyautogui.press('Enter')
                  sleep(5)
                  ## Clicking on SpectLab Run ##
                  SpectLab_AutoRun    = Image.open(BytesIO(base64.b64decode(WhereToClick_Buttons.SpectLab_AutoRun)))                  
                  location                = pyautogui.locateCenterOnScreen(SpectLab_AutoRun, grayscale=True, confidence=0.8)
                  if self.location_error(location) == 1: return
                  pyautogui.moveTo(location.x, location.y, 1)
                  pyautogui.click()
                  
      def ConfigSpectLab2(self):
            if self.CheckSpectLabCheckBox() == 1:
                  print("Range measurement. Saving SpectLab measurement.")
                  ## Clicking on SpectLab disconnect ##
                  SpectLab_Save    = Image.open(BytesIO(base64.b64decode(WhereToClick_Buttons.SpectLab_disconnect)))
                  location          = pyautogui.locateCenterOnScreen(SpectLab_Save, grayscale=False, confidence=0.8)
                  if self.location_error(location) == 1: return
                  pyautogui.moveTo(location.x, location.y, 1)
                  pyautogui.click()
                  sleep(1)
                  ## Clicking on SpectLab Save ##
                  SpectLab_Save    = Image.open(BytesIO(base64.b64decode(WhereToClick_Buttons.SpectLab_save)))
                  location          = pyautogui.locateCenterOnScreen(SpectLab_Save, grayscale=True, confidence=0.7)
                  if self.location_error(location) == 1: return
                  pyautogui.moveTo(location.x, location.y, 1)
                  pyautogui.click()
                  sleep(1)
                  ## Writing file name ##
                  pyautogui.write(self.FileStringEntry.get() + str(int(self.CurrentTargetTemp)) + "C.txt", interval=0.1)
                  sleep(1)
                  pyautogui.press('Enter')
                                  
      def location_error(self, location):
            if location is None: 
                  current_time = time.strftime("%H:%M:%S", time.localtime())
                  self.error_str += current_time + " " + str(self.CurrentTargetTemp) + " IVMaster start button location is not found.\n"
                  print ("SpectLab button location is not found.")
                  self.OverallError = 1
                  return 1
                  
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
            ErrorWindow.title("Summary and Errors")
            ErrorWindow.minsize(350,250)
            ErrorText = tkinter.Text(ErrorWindow, width = 60, height = 30)
            ErrorText.grid(column= 0, row = 0)
            ErrorText.insert(END, self.error_str)

