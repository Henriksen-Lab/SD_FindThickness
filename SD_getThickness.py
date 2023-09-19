'''
Author: Shilling Du, 20230915
'''
import sys, os, time, threading
from tkinter import *
import tkinter as tk
from tkinter.filedialog import askopenfilename, askdirectory
from PIL import Image, ImageTk
import tkinter.simpledialog
import pickle

from UI_subclass import *
from Convert_RGB_to_Wavelength import *

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

    img_list=[]
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
            img_list.append(self)
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
            self.x_entry = EntryBoxH(self, 'X=', initial_value='',width=70,box_color = box_color_1)
            self.x_entry.grid(row=0, column=1, sticky='ew')
            self.y_entry = EntryBoxH(self, 'Y=', initial_value='',width=70,box_color = box_color_1)
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
                frame,
                bg=box_color,
            )
            table_list.append(self)
            self.grid(
                row=row, column=column,
                rowspan=rowspan, columnspan=columnspan,
                ipadx=0, ipady=0,
                padx=0, pady=0,
                sticky='news'
            )
            self.cali_path_entry = EntryBox(self, 'Calibration file path', initial_value='Please choose calibration file path',width=width,box_color=box_color_3)
            self.cali_path_entry.grid(row=0, column=0, sticky='ew')
            def choose_file():
                select_directory = askopenfilename(title="Choose the file")
                self.cali_path_entry.entry.delete(0, 'end')
                self.cali_path_entry.entry.insert(0, select_directory)
            self.cali_path = ttk.Button(
                self,
                text="choose File",
                command=choose_file,
                padding=4
            )
            self.cali_path.grid(row=0, column=0, sticky='ne')
            add_point()
    
    save_list = []
    class SaveFrame(tk.Frame):
        def __init__(self, frame, width, height, row, column, rowspan=1, columnspan=1):
            super().__init__(
                frame, width=width, height=height,
                bg=box_color,
                highlightbackground=border_color,
                highlightcolor=highlight_border_color,
                highlightthickness=1.5,
                bd=6
            )
            save_list.append(self)
            self.grid(
                row=row, column=column,
                rowspan=rowspan, columnspan=columnspan,
                ipadx=frame_ipadx, ipady=frame_ipady,
                padx=frame_padx, pady=frame_pady,
                sticky='new'
            )
            
            self.save_path_entry = EntryBox(self, 'Save file folder path', initial_value='Please choose folder location',width=width-50,box_color=box_color_3)
            self.save_path_entry.grid(row=0, column=0, sticky='ew')
            def choose_folder():
                select_directory = askdirectory(title="Choose the folder")
                self.save_path_entry.entry.delete(0, 'end')
                self.save_path_entry.entry.insert(0, select_directory)
            self.save_path = ttk.Button(
                self,
                text="choose Folder",
                command=choose_folder,
                padding=4
            )
            self.save_path.grid(row=0, column=0, sticky='ne')
            self.filename_entry = EntryBoxH(self,'File name',initial_value='name me please',width=width-50,box_color=box_color_3)
            self.filename_entry.grid(row=1, column=0, sticky='nwe')
            def save_info():
                save_info_to_file()
            self.save_button = ttk.Button(
                self,
                text="Save file",
                command=save_info,
                padding=4
            )
            self.save_button.grid(row=1, column=0, sticky='ne')

    class ScrollableInfoFrame(tk.Frame):
            def __init__(self, master, width, height):
                tk.Frame.__init__(self, master, width=width, height=height)
                self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff", highlightthickness=0)
                self.frame = tk.Frame(self.canvas, background="#ffffff")
                self.hsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
                self.canvas.configure(xscrollcommand=self.hsb.set)

                self.hsb.pack(side=RIGHT, fill="y")
                self.canvas.pack(side=tk.RIGHT, fill="both", expand=True)
                self.canvas.create_window((16, 8), window=self.frame, anchor="nw", tags="self.frame")

                self.frame.bind("<Configure>", self.onFrameConfigure)
                self.pack_propagate(False)

                self.info_frame = StyleFrame(
                    self.frame,
                    label='Info',
                    width=width,
                    height=height
                )
                self.info_frame.pack(side=tk.LEFT, expand=True)

            def onFrameConfigure(self, event):
                '''Reset the scroll region to encompass the inner frame'''
                self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    global i
    i = 1
    def add_point():
        global i
        label = 'P' + str(i)        
        SingleLine(table_list[0],label=label,row=i,column=0)
        i += 1 

    def update_info(x,y,r,g,b):
        basepoint = 0.0
        calibration = False
        def set(item,value,tag=0):
            item.delete(tag, 'end')
            item.insert(tag, value)
        path = img_list[0].dir_entry.entry.get()
        name = (path.split("\\")[-1]).split("/")[-2] + '_' + (path.split("\\")[-1]).split("/")[-1]
        newname = 'SDthickness_'+ name.split('.')[0]
        set(save_list[0].filename_entry.entry,f'{newname}')
        for point in point_list:
            realvalue = point.realvalue_entry.entry.get()
            if realvalue != 'None':
                if float(realvalue) == 0.0:
                    basepoint = float(point.wavelength_entry.entry.get())
                    if table_list[0].cali_path_entry.entry.get() != 'Please choose calibration file path' or table_list[0].cali_path_entry.entry.get() != '':
                        calibration = True
        for point in point_list:
            if point.x_entry.entry.get()=='' or point.y_entry.entry.get()=='':
                set(point.x_entry.entry,x)
                set(point.y_entry.entry,y)
                set(point.rgb_entry.entry,f'{r},{g},{b}')
                wavelength = rgb2wavelength(r,g,b)
                set(point.wavelength_entry.entry,f'{wavelength}')
                if basepoint != 0.0:
                    if not calibration:
                        thickness = wavelength - basepoint
                    else:
#                       try:
                        path = table_list[0].cali_path_entry.entry.get()
                        print(path)
                        with open(path, 'rb') as f:
                            cali_dict = pickle.load(f)
                            print('Calibration loaded')
                        popt = cali_dict['popt']
                        sigma = cali_dict['sigma']
                        def function(x,a,b,c):
                            return a*x**2 + b*x +c
                        thickness = function(wavelength,*popt) - function(basepoint,*popt)
                        print(function(wavelength,*popt),basepoint)
                        print('thickness = ', thickness)
                        print('sigma = ', f'{sigma:.2f}', ' nm')
#                       except:
#                           print('Calibration failed to import')
                    set(point.estimate_entry.entry,f'{thickness}')
                break
    def save_info_to_file():
        dataToSave = {}
        dataToSave.update({'file_path':img_list[0].dir_entry.entry.get()})
        dataToSave.update({'Calib_path':table_list[0].cali_path_entry.entry.get()})
        dataToSave.update({'Point_info':{}})
        i = 0
        for point in point_list:
            if point.x_entry.entry.get()!='' and point.y_entry.entry.get()!='':
                i += 1
                data = {}
                data.update({'x':point.x_entry.entry.get()})
                data.update({'y':point.y_entry.entry.get()})
                data.update({'rgb':point.rgb_entry.entry.get()})
                data.update({'wavelength':point.wavelength_entry.entry.get()})
                data.update({'estimate_t':point.estimate_entry.entry.get()})
                data.update({'real_t':point.realvalue_entry.entry.get()})
                point_name = 'P' + str(i)
                dataToSave['Point_info'].update({point_name:data})
        print(dataToSave)
        folder = save_list[0].save_path_entry.entry.get()
        name = save_list[0].filename_entry.entry.get()
        file_path = os.path.join(folder,name)
        with open(file_path,'wb') as f:
            pickle.dump(dataToSave, f)
        
    def initialize():
        # t = threading.Thread(target=background)
        # t.daemon = True
        # t.start()
        msg = MsgFrame(
            window,
            width=900,
            height=sizey-50,
            column=0, row=0,
            rowspan=2
        )
        scrollable_frame = ScrollableInfoFrame(window,width=sizex-960,height=int(sizey/5)*4 - 20)
        scrollable_frame.grid(column=1, row=0)
        info_frame = scrollable_frame.info_frame
        info = InfoFrame(
            info_frame,
            width=sizex-1000,
            height=int(sizey/5)*4 - 20,
            column=0, row=1
        )
        save = SaveFrame(
            window,
            width=sizex-960,
            height=int(sizey/5)-20,
            column=1, row=1,
        )
    window.after(50, initialize)
    window.mainloop()

main_window()