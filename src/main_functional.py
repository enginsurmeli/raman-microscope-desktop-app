# Importing all the necessary libraries
import sys
import os
from PIL import Image, ImageTk
# import PIL.Image
# import PIL.ImageTk
import time

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import customtkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)  # type: ignore
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.widgets import SpanSelector
from matplotlib.backend_bases import key_press_handler

import numpy as np

import random
import serial
import serial.tools.list_ports as list_ports
import json

import cv2
from pygrabber.dshow_graph import FilterGraph  # pip install pygrabber

# Modes: "System" (standard), "Dark", "Light"
from typing import Optional, Tuple, Union


class MenuBar(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        settings_button = customtkinter.CTkButton(
            self, text="Settings", command=SettingsWindow)
        settings_button.pack(side="bottom", padx=10, pady=10)


class Logo(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.menu_logo_image = customtkinter.CTkImage(Image.open(
            os.path.join(master.image_path, "lst_logo.png")), size=(master.winfo_width(), 53*master.winfo_width()/131))
        self.menu_logo = customtkinter.CTkLabel(
            self, image=self.menu_logo_image, text='')
        self.menu_logo.pack(fill="both", expand=True)


class SerialConsole(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class CameraView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.label = customtkinter.CTkLabel(self, text="")
        self.label.pack(fill="both", expand=True)
        
    def update(self, input_text: str):
        self.label.configure(text=input_text)

class ScanParameters(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class CNCButtons(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class RamanMapSpectrum(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class CNCStatus(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)


class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Settings")
        self.deiconify()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_window_width = 600
        app_window_height = 240
        self.geometry(
            f"{app_window_width}x{app_window_height}+{int(screen_width/2-app_window_width/2)}+{int(screen_height/2-app_window_height/2)}")
        self.resizable(False, False)
        self.grab_set()

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1, 2), weight=0)

        ok_button = customtkinter.CTkButton(
            self, text="OK", command=self.apply_settings)
        ok_button.grid(row=1, column=1, padx=10, pady=10)

        cancel_button = customtkinter.CTkButton(
            self, text="Cancel", command=self.destroy)
        cancel_button.grid(row=1, column=2, padx=10, pady=10)

        self.settings_frame = customtkinter.CTkFrame(self)
        self.settings_frame.grid(
            row=0, column=0, columnspan=3, padx=10, pady=10)

        self.settings_frame.grid_rowconfigure((0, 1, 2, 3, 4), weight=0)
        self.settings_frame.grid_columnconfigure((0, 1, 2, 3), weight=0)

        # create labels and separators
        serial_port_label = customtkinter.CTkLabel(
            self.settings_frame, text="Serial Port")
        serial_port_label.grid(row=0, column=0, padx=10, pady=10)
        separator_1 = ttk.Separator(
            self.settings_frame, orient="horizontal")
        separator_1.grid(row=1, column=0, columnspan=4,
                         padx=10, pady=5, sticky="ew")
        camera_label = customtkinter.CTkLabel(
            self.settings_frame, text="Camera")
        camera_label.grid(row=2, column=0, padx=10, pady=10)
        separator_2 = ttk.Separator(self.settings_frame, orient="horizontal")
        separator_2.grid(row=3, column=0, columnspan=4,
                         padx=10, pady=5, sticky="ew")
        appearance_label = customtkinter.CTkLabel(
            self.settings_frame, text="Appearance")
        appearance_label.grid(row=4, column=0, padx=10, pady=10)

        # list available serial ports
        myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        self.ports_list = [p[0] for p in myports]
        self.serial_ports_combobox = customtkinter.CTkOptionMenu(
            self.settings_frame, values=self.ports_list)
        self.serial_ports_combobox.grid(row=0, column=1, padx=10, pady=10)

        # create a list of baud rates
        baud_rates = ["9600", "19200", "38400", "57600", "115200"]
        self.baud_rates_combobox = customtkinter.CTkOptionMenu(
            self.settings_frame, values=baud_rates)
        self.baud_rates_combobox.grid(row=0, column=2, padx=10, pady=10)

        # create a list of line endings
        line_endings = ["None", "CR", "LF", "Both CR&LF"]
        self.line_endings_combobox = customtkinter.CTkOptionMenu(
            self.settings_frame, values=line_endings)
        self.line_endings_combobox.grid(row=0, column=3, padx=10, pady=10)

        # get a list of available video devices
        self.graph = FilterGraph()

        # fill combobox with video devices
        self.camera_list = self.graph.get_input_devices()
        self.camera_combobox = customtkinter.CTkOptionMenu(
            self.settings_frame, values=self.camera_list, dynamic_resizing=False)
        self.camera_combobox.grid(row=2, column=1, padx=10, pady=10)

        self.appearance_combobox = customtkinter.CTkOptionMenu(
            self.settings_frame, values=["Light", "Dark", "System"])
        self.appearance_combobox.grid(row=4, column=1, padx=10, pady=10)

        # set current values
        self.serial_ports_combobox.set(App.serial_port)
        self.baud_rates_combobox.set(App.baudrate)
        self.line_endings_combobox.set(App.serial_line_ending)
        self.camera_combobox.set(App.camera)
        self.appearance_combobox.set(App.appearance)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        
    def connect_camera_event(self):
        for i, device in enumerate(self.camera_list):   
            if device == self.camera_combobox.get():
                App.camera = i


    def apply_settings(self):
        # apply changes
        CameraView.update("Text changed")
        self.connect_camera_event()        
        App.appearance = self.appearance_combobox.get()
        self.change_appearance_mode_event(App.appearance)

        # save settings to json file
        data = {}
        data['lineending'] = self.line_endings_combobox.get()
        data['baudrate'] = self.baud_rates_combobox.get()
        data['port'] = self.serial_ports_combobox.get()
        data['portlist'] = self.ports_list
        data['camera'] = App.camera
        data['cameralist'] = self.camera_list
        data['appearance'] = App.appearance
        with open('app_settings.json', 'w') as jfile:
            json.dump(data, jfile, indent=4)
            jfile.close()
        self.destroy()


# class QuitAppWindow(customtkinter.CTkToplevel):
#     def __init__(self):
#         super().__init__()

#         self.geometry("320x100")
#         self.title("Quit Application")
#         self.resizable(False, False)
#         self.deiconify()
#         self.grab_set()

#         label = customtkinter.CTkLabel(
#             self, text="Are you sure you want to quit?")
#         label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
#         yes_button = customtkinter.CTkButton(
#             self, text="Yes", command=self._quit)
#         yes_button.grid(row=1, column=0, padx=10, pady=10)
#         no_button = customtkinter.CTkButton(
#             self, text="No", command=self.destroy)
#         no_button.grid(row=1, column=1, padx=10, pady=10)

#     def _quit():
#         App.quit()
#         App.destroy()


class App(customtkinter.CTk):

    current_folder = os.getcwd()
    # current_folder = globals()['_dh'][0]
    settings_data = {}
    filename = sys.argv[0].rsplit('.', 1)[0]
    jfile = None
    try:
        jfile = open('app_settings.json')
        settings_data = json.load(jfile)
    except FileNotFoundError as fnfe:
        pass
    if jfile:
        jfile.close()

    serial_line_ending = settings_data.get('lineending', 'CR')
    baudrate = settings_data.get('baudrate', '115200')
    serial_port = settings_data.get('port', 'COM7')
    camera = settings_data.get('camera', '0')
    appearance = settings_data.get('appearance', 'System')

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.OnQuitApp)
        self.title("LST Raman Microscope Scanner")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_window_width = 1280
        app_window_height = 720
        self.geometry(
            f"{app_window_width}x{app_window_height}+{int(screen_width/2-app_window_width/2)}+{int(screen_height/2-app_window_height/2)}")
        self.minsize(app_window_width, app_window_height)
        self.grab_set()
        icons_folder = 'icons'
        self.image_path = os.path.join(App.current_folder, icons_folder)

        try:
            # self.iconbitmap(os.path.join(self.image_path, "microscope_logo.ico"))
            iconpath = ImageTk.PhotoImage(file=os.path.join(self.image_path, "microscope_logo.png"))
            self.wm_iconbitmap()
            self.after(300, lambda: self.iconphoto(False, iconpath))
        except:
            pass

        # set grid layout 2x4
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=7)
        self.grid_rowconfigure(2, weight=2)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=2)

        # create frames
        self.menu_bar_frame = MenuBar(self)
        self.menu_bar_frame.grid(
            row=0, column=0, rowspan=2, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.logo_frame = Logo(self)
        self.logo_frame.grid(row=2, column=0, padx=(
            20, 10), pady=(10, 20), sticky="nsew")

        self.raman_map_spectrum_frame = RamanMapSpectrum(self)
        self.raman_map_spectrum_frame.grid(
            row=0, column=1, rowspan=3, padx=10, pady=20, sticky="nsew")

        self.camera_view_frame = CameraView(self)
        self.camera_view_frame.grid(
            row=0, column=2, rowspan=2, padx=10, pady=(20, 10), sticky="nsew")

        self.serial_console_frame = SerialConsole(self)
        self.serial_console_frame.grid(
            row=2, column=2, padx=10, pady=(10, 20), sticky="nsew")

        self.cnc_status_frame = CNCStatus(self)
        self.cnc_status_frame.grid(row=0, column=3, padx=(
            10, 20), pady=(20, 10), sticky="nsew")

        self.cnc_buttons_frame = CNCButtons(self)
        self.cnc_buttons_frame.grid(
            row=1, column=3, rowspan=2, padx=(10, 20), pady=(10, 20), sticky="nsew")

        # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_appearance_mode(App.appearance)
        # Themes: "blue" (standard), "green", "dark-blue"
        customtkinter.set_default_color_theme("blue")
        # customtkinter.deactivate_automatic_dpi_awareness()

    def OnQuitApp(self):
        quit_app_window = customtkinter.CTkToplevel(self)
        quit_app_window.geometry(
            f"320x100+{self.winfo_x()+self.winfo_width()//2-160}+{self.winfo_y()+self.winfo_height()//2-50}")
        quit_app_window.title("Quit Application")
        quit_app_window.resizable(False, False)
        quit_app_window.deiconify()
        quit_app_window.grab_set()

        label = customtkinter.CTkLabel(
            quit_app_window, text="Are you sure you want to quit?")
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        yes_button = customtkinter.CTkButton(
            quit_app_window, text="Yes", command=self._quit)
        yes_button.grid(row=1, column=0, padx=10, pady=10)
        no_button = customtkinter.CTkButton(
            quit_app_window, text="No", command=quit_app_window.destroy)
        no_button.grid(row=1, column=1, padx=10, pady=10)

    def _quit(self):
        self.quit()
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
