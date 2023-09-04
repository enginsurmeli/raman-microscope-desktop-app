# Importing all the necessary libraries
import sys
import os
from PIL import ImageTk

import customtkinter

import json

import quit_app_window
import cnc_buttons
import serial_console
import camera_view
import raman_plot
import raman_search


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
        self.grid_rowconfigure((0, 2), weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_columnconfigure((0, 2), weight=1)
        self.grid_columnconfigure(1, weight=9)

        # create frames
        self.cnc_buttons_frame = cnc_buttons.CNCButtons(self)
        self.cnc_buttons_frame.grid(
            row=0, column=0, rowspan=2, padx=(20, 10), pady=(20, 10), sticky="nsew")

        self.serial_console_frame = serial_console.SerialConsole(self)
        self.serial_console_frame.grid(
            row=2, column=0, padx=(20, 10), pady=(10, 20), sticky="nsew")

        self.raman_plot_frame = raman_plot.RamanPlot(
            self)
        self.raman_plot_frame.grid(
            row=0, column=1, rowspan=3, padx=10, pady=20, sticky="nsew")

        self.camera_view_frame = camera_view.CameraView(self)
        self.camera_view_frame.grid(
            row=0, column=2, padx=(10, 20), pady=(20, 10), sticky="nsew")

        self.raman_search_frame = raman_search.RamanSearch(self)
        self.raman_search_frame.grid(
            row=1, column=2, rowspan=2, padx=(10, 20), pady=(10, 20), sticky="nsew")

        # Placeholder labels for the frames
        self.raman_plot_frame_label = customtkinter.CTkLabel(
            self.raman_plot_frame, text="Raman Plot")
        self.raman_plot_frame_label.place(relx=0.5, rely=0.5, anchor="center")

        self.camera_view_frame_label = customtkinter.CTkLabel(
            self.camera_view_frame, text="Camera View")
        self.camera_view_frame_label.place(relx=0.5, rely=0.5, anchor="center")

        self.raman_search_frame_label = customtkinter.CTkLabel(
            self.raman_search_frame, text="Raman Search")
        self.raman_search_frame_label.place(
            relx=0.5, rely=0.5, anchor="center")

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

        self.updateSettings(settings_data)

    def updateSettings(self, settings_data: dict):
        self.settings_data = settings_data
        serial_line_ending = settings_data.get('lineending')
        baudrate = settings_data.get('baudrate')
        serial_port = settings_data.get('port')
        camera = settings_data.get('camera_index')
        appearance = settings_data.get('appearance')

        # change serial settings
        self.serial_console_frame.updateSerialSettings(
            serial_port=serial_port, baudrate=baudrate, line_ending=serial_line_ending)

        # change camera settings

        # set theme and appearance mode
        customtkinter.set_appearance_mode(appearance)
        customtkinter.set_default_color_theme("blue")
        # customtkinter.deactivate_automatic_dpi_awareness()

    def sendSettingsData(self):
        return self.settings_data

    def sendSerialCommand(self, command: str):
        self.serial_console_frame.send(cnc_command=command)

    # def resetSerialConnection(self):
    #     self.serial_console_frame.resetSerialConnection()

    def OnQuitApp(self):
        quit_app = quit_app_window.OnQuitApp(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
