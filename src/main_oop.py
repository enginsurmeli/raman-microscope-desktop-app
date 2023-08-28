# Importing all the necessary libraries
import sys
import os
from PIL import ImageTk

import customtkinter

import json

import quit_app_window
import menu
import logo
import cnc_status
import cnc_buttons
import serial_console
import camera_view
import scan_parameters
import raman_map_spectrum


class App(customtkinter.CTk):

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

        self.current_folder = os.getcwd()
        # self.current_folder = globals()['_dh'][0] # Use this for jupyter notebook
        self.filename = sys.argv[0].rsplit('.', 1)[0]
        icons_folder = 'src//icons'
        self.image_path = os.path.join(self.current_folder, icons_folder)

        try:
            # self.iconbitmap(os.path.join(self.image_path, "microscope_logo.ico"))
            iconpath = ImageTk.PhotoImage(file=os.path.join(
                self.image_path, "microscope_logo.png"))
            self.wm_iconbitmap()
            self.after(300, lambda: self.iconphoto(False, iconpath))
        except:
            pass

        # set grid layout 3x4
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=7)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=8)
        self.grid_columnconfigure(2, weight=2)
        self.grid_columnconfigure(3, weight=2)

        # create frames
        self.menu_bar_frame = menu.Menu(self)
        self.menu_bar_frame.grid(
            row=0, column=0, rowspan=2, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.logo_frame = logo.Logo(self)
        self.logo_frame.grid(row=2, column=0, padx=(
            20, 10), pady=(10, 20), sticky="nsew")

        self.raman_map_spectrum_frame = raman_map_spectrum.RamanMapSpectrum(
            self)
        self.raman_map_spectrum_frame.grid(
            row=0, column=1, rowspan=3, padx=10, pady=20, sticky="nsew")

        self.camera_view_frame = camera_view.CameraView(self)
        self.camera_view_frame.grid(
            row=0, column=2, rowspan=2, padx=10, pady=(20, 10), sticky="nsew")

        self.serial_console_frame = serial_console.SerialConsole(self)
        self.serial_console_frame.grid(
            row=2, column=2, padx=10, pady=(10, 20), sticky="nsew")

        self.cnc_status_frame = cnc_status.CNCStatus(self)
        self.cnc_status_frame.grid(row=0, column=3, padx=(
            10, 20), pady=(20, 10), sticky="nsew")

        self.cnc_buttons_frame = cnc_buttons.CNCButtons(self)
        self.cnc_buttons_frame.grid(
            row=1, column=3, rowspan=2, padx=(10, 20), pady=(10, 20), sticky="nsew")
        
        self.initializeSettings()

    def initializeSettings(self):
        settings_data = {}
        jfile = None
        try:
            jfile = open('settings.json')
            settings_data = json.load(jfile)
        except FileNotFoundError as fnfe:
            pass
        if jfile:
            jfile.close()

        self.serial_line_ending = settings_data.get('lineending', 'CR')
        self.baudrate = settings_data.get('baudrate', '115200')
        self.serial_port = settings_data.get('port', 'COM7')
        self.camera = settings_data.get('camera', '0')
        self.appearance = settings_data.get('appearance', 'Dark')

        customtkinter.set_appearance_mode(self.appearance)
        customtkinter.set_default_color_theme("blue")
        # customtkinter.deactivate_automatic_dpi_awareness()

        return settings_data
    
    def updateSettings(self):
        print(f"{self.serial_port}, {self.baudrate}, {self.serial_line_ending}, {self.camera}, {self.appearance}")

    def OnQuitApp(self):
        quit_app = quit_app_window.OnQuitApp(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
