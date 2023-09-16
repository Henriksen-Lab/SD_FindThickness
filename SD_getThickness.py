'''
Author: Shilling Du, 20230915
'''
import sys, os, time, threading
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import tkinter.simpledialog
from UI_subclass import *


def background():
        pass

def main_window():
    # Window
    window = tk.Tk()
    window.title('Get thickness from image')
    window.geometry(f'{sizex}x{sizey}')
    window.configure(bg = background_color)
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=4)
    window.rowconfigure(0, weight=1)
    window.rowconfigure(1, weight=4)

    class MsgFrame(tk.Frame):
        def __init__(self, frame, width, height, row, column, rowspan=1, columnspan=1):
            super().__init__(
                frame, width=width, height=height,
                bg=box_color,
                highlightbackground=border_color,
                highlightcolor=highlight_border_color,
                highlightthickness=1.5,
                bd=6
            )
            self.grid(
                row=row, column=column,
                rowspan=rowspan, columnspan=columnspan,
                ipadx=frame_ipadx, ipady=frame_ipady,
                padx=frame_padx, pady=frame_pady,
                sticky='nw'
            )
        
            self.dir_entry = EntryBox(self, 'Image path', initial_value='Please choose image location',width=width,box_color=box_color_3)
            self.dir_entry.grid(row=0, column=0, sticky='ew')
            img = None
            def choose_file():
                global img
                select_directory = askopenfilename(title="Choose the file")
                self.dir_entry.entry.delete(0, 'end')
                self.dir_entry.entry.insert(0, select_directory)
                original = Image.open(select_directory)
                original = original.resize((900,672)) #resize image
                img = ImageTk.PhotoImage(original)
                self.canvas.create_image(0, 0, image=img, anchor="nw")
                self.canvas.update()
            self.file_path = ttk.Button(
                self,
                text="choose File",
                command=choose_file,
                padding=4
            )
            self.file_path.grid(row=0, column=0, sticky='ne')
            self.canvas = Canvas(self, width=900, height=672)
            self.canvas.grid(row=1, column=0, sticky='nw')

            def getxy(eventclick):
                x = eventclick.x
                y = eventclick.y
                original = Image.open(self.dir_entry.entry.get())
                original = original.resize((900,672)) #resize image
                r, g, b = original.getpixel((x, y))
                update_info(x,y,r,g,b)
                # print('X = ',x,',Y = ',y)
                # print('rgb = ',r,g,b)
            # Double mouse click event
            self.canvas.bind("<Double-Button-1>", getxy)
    
    
    point_list = []
    class SingleLine(tk.Frame):
        def __init__(self, frame, label, row, column,rowspan=1, columnspan=1):
            super().__init__(
                frame,
                bg=box_color,
            )
            self.grid(
                row=row, column=column,
                rowspan=rowspan, columnspan=columnspan,
                ipadx=0, ipady=0,
                padx=0, pady=0,
                sticky='nw'
            )
            point_list.append(self)
            self.label = tk.Label(self,text=label,bg=box_color)
            self.label.grid(row=0,column=0)
            self.x_entry = EntryBoxH(self, 'X=', initial_value='?',width=70,box_color = box_color_1)
            self.x_entry.grid(row=0, column=1, sticky='ew')
            self.y_entry = EntryBoxH(self, 'Y=', initial_value='?',width=70,box_color = box_color_1)
            self.y_entry.grid(row=1, column=1, sticky='ew')
            self.rgb_entry = EntryBoxH(self, 'RGB=', initial_value='0,0,0',width=140)
            self.rgb_entry.grid(row=0, column=2, sticky='ew')
            self.wavelength_entry = EntryBoxH(self, 'lamda(nm) =', initial_value=0, width=140)
            self.wavelength_entry.grid(row=0, column=3, sticky='ew')
            self.estimate_entry = EntryBoxH(self, 'Estimated t=', initial_value='None',width=140)
            self.estimate_entry.grid(row=1, column=2, sticky='ew')
            self.realvalue_entry = EntryBoxH(self, 'Real t=', initial_value='None',width=140)
            self.realvalue_entry.grid(row=1, column=3, sticky='ew')
            def add_point_trigger():
                add_point()
            self.add_button = ttk.Button(self,text="+", command=add_point_trigger,width=1)
            self.add_button.grid(row=1,column=0)
    
    
    table_list = []
    class InfoFrame(tk.Frame):
        def __init__(self, frame, width, height, row, column, rowspan=1, columnspan=1):
            super().__init__(
                frame, width=width, height=height,
                bg=box_color,
                highlightbackground=border_color,
                highlightcolor=highlight_border_color,
                highlightthickness=1.5,
                bd=6
            )
            table_list.append(self)
            self.grid(
                row=row, column=column,
                rowspan=rowspan, columnspan=columnspan,
                ipadx=frame_ipadx, ipady=frame_ipady,
                padx=frame_padx, pady=frame_pady,
                sticky='nw'
            )
            self.cali_path_entry = EntryBox(self, 'Calibration file path', initial_value='Please choose calibration file path',width=width,box_color=box_color_3)
            self.cali_path_entry.grid(row=0, column=0, sticky='ew')
            def choose_file():
                select_directory = askopenfilename(title="Choose the file")
                self.cali_path_entry.entry.delete(0, 'end')
                self.cali_path_entry.insert(0, select_directory)
            self.cali_path = ttk.Button(
                self,
                text="choose File",
                command=choose_file,
                padding=4
            )
            self.cali_path.grid(row=0, column=0, sticky='ne')
            add_point()
    
    global i
    i = 1
    def add_point():
        global i
        label = 'P' + str(i)        
        SingleLine(table_list[0],label=label,row=i,column=0)
        i += 1 
        
    def update_info(x,y,r,g,b):
        def set(item,value,tag=0):
            item.delete(tag, 'end')
            item.insert(tag, value)
        for point in point_list:
            if point.x_entry.entry.get()=='?' or point.y_entry.entry.get()=='?':
                set(point.x_entry.entry,x)
                set(point.y_entry.entry,y)
                set(point.rgb_entry.entry,f'{r},{g},{b}')
                pass


    def reply_handler():
        global reply
        pass
        window.after(50, reply_handler)

    def initialize():
        t = threading.Thread(target=background)
        t.daemon = True
        t.start()

        msg = MsgFrame(
            window,
            width=900,
            height=sizey-50,
            column=0, row=0
        )
        table = InfoFrame(
            window,
            width=sizex-1000,
            height=sizey-50,
            column=1, row=0
        )

        window.after(50, reply_handler)
    window.after(50, initialize)
    window.mainloop()

def getRGB(img,x,y):
    pass

main_window()