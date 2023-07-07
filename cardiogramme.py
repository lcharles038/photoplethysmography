import serial
import time
from tkinter import *

arduino = serial.Serial('/dev/cu.usbmodem14101',9600,timeout=.1)

window = Tk()

class EG:
    def __init__(self, window, canvas_width, canvas_height, scale_x, scale_y):
        self.old_dot = [0,0]
        self.new_dot = [0,0]
        self.scale_x = scale_x
        self.scale_y = scale_y
        self.offset_y = 0
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.canvas = Canvas(window, width=self.canvas_width, height=self.canvas_height, background='white')
        self.canvas.pack()

    def print_data(self, data, width, color):
        self.new_dot[0] = self.old_dot[0]+self.scale_x
        self.new_dot[1] = data
        self.canvas.create_line(self.old_dot[0], self.old_dot[1], self.new_dot[0], self.new_dot[1], width=width, fill=color)
        self.old_dot[0] = self.new_dot[0]
        self.old_dot[1] = self.new_dot[1]

class ECG(EG):
    def __init__(self, window, canvas_width, canvas_height, scale_x, scale_y):
        self.threshold = 0
        self.threshold_pc = 0
        super(ECG, self).__init__(window, canvas_width, canvas_height, scale_x, scale_y)
        self.threshold_line = self.canvas.create_line(0,self.threshold,self.canvas_width,self.threshold,fill='blue')

    # data : 0-1024 (arduino 0-5v)
    def print_data(self,data):
        if self.old_dot[0]+self.scale_x > self.canvas_width:
            self.old_dot[0] = 0
            self.canvas.delete("all")
            self.threshold_line = self.canvas.create_line(0,self.threshold,self.canvas_width,self.threshold,fill='blue')
        data = self.canvas_height - data/1024*self.canvas_height*self.scale_y/100 - self.offset_y
        super(ECG,self).print_data(data, 1.0, 'red')

    def update_threshold(self, threshold):
        self.threshold_pc = threshold
        self.threshold = self.canvas_height - threshold/100*self.canvas_height
        self.canvas.coords(self.threshold_line,0,self.threshold,self.canvas_width,self.threshold)


class BPM_EG(EG):
    def __init__(self, window, canvas_width, canvas_height, scale_x, scale_y):
        super(BPM_EG, self).__init__(window, canvas_width, canvas_height, scale_x, scale_y)
        self.old_dot[0] = 40
        self.print_items()

    # data : bpm
    def print_data(self, data):
        if self.old_dot[0]+self.scale_x > self.canvas_width:
            self.old_dot[0] = 40
            self.canvas.delete("all")
            self.print_items()
        data = self.canvas_height*(1-0.8/90*(data-28.75)) # offset=28.75 bpm ; px/bpm=cavnas_height*0.8/3/30
        super(BPM_EG,self).print_data(data, 2.0, 'blue')

    def print_items(self):
        for i in range(4):
            self.canvas.create_text(20, self.canvas_height*(0.8/3*i+0.1), text=str(130-i*30))
            self.canvas.create_line(40, self.canvas_height*(0.8/3*i+0.1), self.canvas_width, self.canvas_height*(0.8/3*i+0.1))

class UI:
    eg_select = IntVar()
    bpm_text = StringVar()
    bpm_lock = False
    old_time = time.clock()
    bpm_last = [0,0,0,0,0]

    def __init__(self, window, width, ecg_height, bpm_height):
        self.frame_menu = Frame(window)

        self.eg_menu = Frame(self.frame_menu)

        self.threshold = Scale(self.frame_menu, from_=0, to=100, label="Threshold (%) :", orient=HORIZONTAL, length=width/5, command=self.threshold_callback)
        self.threshold.set(50)
        self.threshold.grid(row=0,column=1)

        self.scale_x = Scale(self.frame_menu, resolution=0.01, from_=0.25, to=2, label="Scale X axis (px/data) :", orient=HORIZONTAL, length=width/5, command=self.scale_x_callback)
        self.scale_x.set(1)
        self.scale_x.grid(row=0,column=2)

        self.scale_y = Scale(self.frame_menu, from_=50, to=400, label="Scale Y axis (%):", orient=HORIZONTAL, length=width/5, command=self.scale_y_callback)
        self.scale_y.set(100)
        self.scale_y.grid(row=0,column=3)

        self.offset_y = Scale(self.frame_menu, from_=-ecg_height, to=ecg_height, label="Offset Y axis (px) :", orient=HORIZONTAL, length=width/5, command=self.offset_y_callback)
        self.offset_y.set(0)
        self.offset_y.grid(row=0,column=4)

        self.bpm_label = Label(self.frame_menu, width=20, textvariable=self.bpm_text)
        self.bpm_label.grid(row=0,column=5)

        self.eg1 = Radiobutton(self.eg_menu, text="ECG", variable=self.eg_select, value=1, command=self.on_change)
        self.eg1.select()
        self.eg1.grid(row=0,column=0)
        self.eg2 = Radiobutton(self.eg_menu, text="Heart Rate", variable=self.eg_select, value=2, command=self.on_change)
        self.eg2.grid(row=1,column=0)
        self.eg_menu.grid(row=0,column=0)

        self.frame_menu.pack()

        self.ecg = ECG(window,window.winfo_screenwidth(),ecg_height, 1, 1)
        self.bpm = BPM_EG(window,window.winfo_screenwidth(),bpm_height, 10, 1)


    def on_change(self):
        if self.eg_select.get() == 1:
            self.scale_x.config(from_=0.25, to=2)
            self.scale_x.set(self.ecg.scale_x)
            self.scale_y.set(self.ecg.scale_y)
            self.offset_y.set(self.ecg.offset_y)
            self.threshold.set(self.ecg.threshold_pc)
        if self.eg_select.get() == 2:
            self.scale_x.config(from_=5, to=20)
            self.scale_x.set(self.bpm.scale_x)

    def threshold_callback(self, threshold):
        if self.eg_select.get() == 1:
            self.ecg.update_threshold(float(threshold))

    def scale_x_callback(self, scale_x):
        if self.eg_select.get() == 1:
            self.ecg.scale_x = float(scale_x)
        if self.eg_select.get() == 2:
            self.bpm.scale_x = float(scale_x)

    def scale_y_callback(self, scale_y):
        if self.eg_select.get() == 1:
            self.ecg.scale_y = float(scale_y)

    def offset_y_callback(self, offset):
        if self.eg_select.get() == 1:
            self.ecg.offset_y = float(offset)

    def ECG_update_BPM(self):
        if(self.ecg.threshold > self.ecg.new_dot[1]):
            if not self.bpm_lock:
                self.new_time = time.clock()
                self.dummy = 1/(self.new_time - self.old_time)*60
                self.bpm_text.set(self.dummy)
                self.bpm_last.append(self.dummy)
                del self.bpm_last[0]
                self.dummy = 0
                for i in range(5):
                    self.dummy += self.bpm_last[i]
                self.dummy /= 5
                self.bpm.print_data(self.dummy)
                self.bpm_lock = True
                self.old_time = self.new_time
        else:
            if self.bpm_lock:
                self.bpm_lock = False


ui = UI(window,window.winfo_screenwidth(),550, 150)


def read_data():
    #data = arduino.read(2)
    #if len(data)==2:
    #    ui.ecg.print_data(data[0]*256+data[1])
    #    ui.ECG_update_BPM()
    #window.after(1,read_data)
    data = arduino.readline();
    if len(data)>0 :
        #print(data)
        #print(data.rstrip().decode())
        ui.ecg.print_data(int(data.rstrip().decode()))
        ui.ECG_update_BPM()
    window.after(1,read_data)

window.after(1,read_data)
window.mainloop()
