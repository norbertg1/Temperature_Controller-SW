from tkinter import *
import tkinter

class MeasureRange():
      def __init__(self):
            i=1


      def OpenMeasureRange(self):
            self.SettingsWindow = tkinter.Tk()
            self.SettingsWindow.title("MeasureRange")
            self.SettingsWindow.minsize(350,250)
            FileStringVar = tkinter.StringVar(self.SettingsWindow,value='default text')
            StartTempVar = tkinter.StringVar(self.SettingsWindow,value='20')
            StepSizeVar = tkinter.StringVar(self.SettingsWindow,value='25')
            EndTempVar = tkinter.StringVar(self.SettingsWindow,value='250')
            MeasurementLengthVar = tkinter.StringVar(self.SettingsWindow,value='20')
            WaitBeforeMeasurementVar = tkinter.StringVar(self.SettingsWindow,value='20')
            
            tkinter.Label(self.SettingsWindow, text = "Name of the file").place(x = 10, y = 0)
            tkinter.Label(self.SettingsWindow, text = "Start Temp.").place(x = 10, y = 50)
            tkinter.Label(self.SettingsWindow, text = "Step size").place(x = 130, y = 50)
            tkinter.Label(self.SettingsWindow, text = "End Temp.").place(x = 230, y = 50)
            tkinter.Label(self.SettingsWindow, text = "Measurement Length").place(x = 10, y = 120)
            tkinter.Label(self.SettingsWindow, text = "Wait Before measurement").place(x = 170, y = 120)
            tkinter.Label(self.SettingsWindow, text = "Status:").place(x = 10, y = 220)
            self.status = tkinter.Label(self.SettingsWindow, text = "Not started", font= ("default", "12", "bold")).place(x = 70, y = 220)
            tkinter.Label(self.SettingsWindow, text = "°C").place(x =100, y = 70)
            tkinter.Label(self.SettingsWindow, text = "°C").place(x = 210, y = 70)
            tkinter.Label(self.SettingsWindow, text = "°C").place(x = 320, y = 70)
            tkinter.Label(self.SettingsWindow, text = "min.").place(x = 130, y = 140)
            tkinter.Label(self.SettingsWindow, text = "min.").place(x = 300, y = 140)
            FileStringEntry = tkinter.Entry(self.SettingsWindow, width = 20, textvariable = FileStringVar).place(x = 10, y = 20)
            StartTempEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = StartTempVar).place(x = 10, y = 70)
            StepEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = StepSizeVar).place(x = 120, y = 70)
            EndTemptEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = EndTempVar).place(x = 230, y = 70)
            MeasureLengthEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = MeasurementLengthVar).place(x = 40, y = 140)
            WaitBeforeMeasurementEntry = tkinter.Entry(self.SettingsWindow, width = 10, textvariable = WaitBeforeMeasurementVar).place(x = 210, y = 140)
            StartButton   = tkinter.Button(self.SettingsWindow, text = "START", command = self.Start, width = 20).place(x = 20, y = 180)
            StartButton   = tkinter.Button(self.SettingsWindow, text = "Next Step", command = self.Start, width = 10).place(x = 220, y = 180)

      def Start(self):
            i=0