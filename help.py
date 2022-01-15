import tkinter
from tkinter.constants import LEFT

def ShowHelp(HelpWindow):
    tkinter.Label(HelpWindow, text =    "Menu:\n\t 0 -> Startup menu, heating or cooling is off\n\t 1 -> Startup menu, Heating or cooling is on\
                                        \n\t 101 -> Kp set menu\n\t 102 -> Kd set menu\n\t 103 -> Ki set menu\
                                        \n\t 104 -> Max power\n\t 105 -> Mode\n\t 106 -> Choose the Sensor\
                                        \n\t 107 -> Choose the PWM frequency (currently the HW doesnt support is)\n\t 108 -> Set the Temperature offset\
                                        \nMode:\n\t -1 -> cooling\n\t 1 -> heating \
                                        \nSensors: \n\t 1 -> NTCS0603E3222FMT\n\t 2 -> NTCG163JX103DTDS\n\t 3 -> NTC_100K\n\t 4 -> PT1000\
                                        \n\nOffset Temp -> Set the offset temperature \nMax. power set -> Set the maximum output power of the device in percents\
                                        \nFreq. -> Output PWM frequency of the microporcessor. Currently the power HW doesnt support changint\
                                        \nKp -> Kp is the Proportional parameter of PID \nKd -> Kd is The Derivative parameter of PID \nKi -> Ki is The Integral parameter of PID\
                                        \nTemp. filter -> The constant for the first order filter of temperature", justify=LEFT).grid(column = 0, row = 0)
