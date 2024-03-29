from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import pyplot
from matplotlib.animation import FuncAnimation
from random import randrange
import numpy
from collections import deque
import matplotlib
from datetime import datetime
import time

nr_points = 1000

matplotlib.use('TkAgg')

class graphicon():
    def __init__(self, window):
        self.starttime = float(round(time.time() * 10)/10)
        self.UpdatedFlag = False
        self.x_data = deque()
        self.x2_data = deque()
        self.y_data = deque()
        self.y2_data = deque()
        self.figure = pyplot.figure()
        plotlays, plotcols = [2], ["red","black"]
        self.lines = []
        ax1 = plt.axes()
        ax1.set_xlabel("Time [s]")
        ax1.set_ylabel("Temperature [°C]")
        self.line, = ax1.plot([], [], lw=1)
        width = [1,0.5]
        style = ["solid", "dashed"]
        for index in range(2):
            lobj = ax1.plot([],[],linestyle=style[index], lw=width[index],color=plotcols[index])[0]
            self.lines.append(lobj)
        canvas = FigureCanvasTkAgg(self.figure, master=window)
        plot_widget = canvas.get_tk_widget()
        plot_widget.place(x = 0, y = 120)
        self.target_temp = 25
    
    def update(self, frame):
        if(len(self.x_data)>=nr_points):
            self.x_data.rotate(-1)
            self.y_data.rotate(-1)
            self.y2_data.rotate(-1)
            self.x_data[nr_points-1] = self.x_temp
            self.y_data[nr_points-1] = self.y_temp
            self.y2_data[nr_points-1] = self.target_temp
            
            self.ylist = [self.y_data, self.y2_data]     
            self.xlist = [self.x_data, self.x_data]
            for lnum,self.line in enumerate(self.lines):
                self.line.set_data(self.xlist[lnum], self.ylist[lnum]) # set data for each line separately. 

            #self.line2.set_data(self.x_data, self.y2_data)
        else:
            try:
                if self.UpdatedFlag is True:
                    self.UpdatedFlag = False
                    self.x_data.append(self.x_temp)
                    self.y_data.append(self.y_temp)
                    self.x2_data.append(self.x_temp)   
                    self.y2_data.append(self.target_temp)
                    self.ylist = [self.y_data, self.y2_data]     
                    self.xlist = [self.x_data, self.x2_data]
                    for lnum,self.line in enumerate(self.lines):
                        self.line.set_data(self.xlist[lnum], self.ylist[lnum]) # set data for each line separately. 
            except:
                return None 
            #self.line[0].set_data(self.xlist[0], self.ylist[0])
            #self.line[1].set_data(self.xlist[1], self.ylist[1])        
            #self.line2.set_data(self.x_data, self.y2_data)        
        self.figure.gca().relim()
        self.figure.gca().autoscale()   
        y = self.figure.gca().get_ylim()
        if(abs(y[0]-y[1]) < 1):             #Limits the maximum autoscale
            y_avg = (y[0]+y[1])/2
            self.figure.gca().set_ylim(y_avg-2,y_avg+2)
        return self.lines

    def updatexy(self,y):
        self.UpdatedFlag = True
        self.x_temp = float(round(time.time() * 10)/10) - self.starttime
        self.y_temp = y
        
    def init(self):
        for self.line in self.lines:
            self.line.set_data([],[])
            return self.lines

    def setTargetTempline(self, targeTemp):
        self.target_temp = targeTemp