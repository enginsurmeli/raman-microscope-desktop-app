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
import raman_scan


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.OnQuitApp)
        self.title("LST Raman Microscope Scanner")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        app_window_width = 1600
        app_window_height = 900
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
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        # create frames
        self.cnc_buttons_frame = cnc_buttons.CNCButtons(self)
        self.cnc_buttons_frame.grid(
            row=0, column=0, rowspan=2, padx=(20, 10), pady=(20, 10), sticky="ns")

        self.raman_scan_frame = raman_scan.RamanScan(self)
        self.raman_scan_frame.grid(row=2, column=0, padx=(20, 10), pady=10)

        self.serial_console_frame = serial_console.SerialConsole(self)
        self.serial_console_frame.grid(
            row=3, column=0, padx=(20, 10), pady=(10, 20), sticky="nsew")

        self.raman_plot_frame = raman_plot.RamanPlot(self)
        self.raman_plot_frame.grid(
            row=0, column=1, rowspan=4, padx=10, pady=20, sticky="nsew")

        self.camera_view_frame = camera_view.CameraView(self)
        self.camera_view_frame.grid(
            row=0, column=2, padx=(10, 20), pady=(20, 10), sticky="nsew")

        self.raman_search_frame = raman_search.RamanSearch(self)
        self.raman_search_frame.grid(
            row=1, column=2, rowspan=3, padx=(10, 20), pady=(10, 20), sticky="nsew")

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
        camera_index = settings_data.get('camera_index')
        appearance = settings_data.get('appearance')
        save_folder = settings_data.get('save_folder')

        # change serial settings
        self.serial_console_frame.updateSerialSettings(
            serial_port=serial_port, baudrate=baudrate, line_ending=serial_line_ending)

        # change camera settings
        self.camera_view_frame.connect_camera(camera_index=camera_index)

        # set theme and appearance mode
        customtkinter.set_appearance_mode(appearance)
        customtkinter.set_default_color_theme("blue")
        # customtkinter.deactivate_automatic_dpi_awareness()

        # change color of treeview and plot area
        color_palette = {'Light': ['#dbdbdb', '#dce4ee', '#1f6aa5', '#252526', '#cfcfcf'], 'Dark': [
            '#2b2b2b', '#252526', '#1f6aa5', '#dce4ee', '#333333']}
        self.raman_search_frame.changeTheme(
            color_palette=color_palette.get(appearance))
        self.raman_plot_frame.changeTheme(
            color_palette=color_palette.get(appearance))

        # change save folder
        self.raman_plot_frame.changeSaveFolder(save_folder=save_folder)

    def sendSettingsData(self):
        return self.settings_data

    def sendSerialCommand(self, command: str):
        self.serial_console_frame.send(cnc_command=command)

    def updateCNCStatus(self, status: str):
        self.cnc_buttons_frame.updateCNCStatus(status)

    # def resetSerialConnection(self):
    #     self.serial_console_frame.resetSerialConnection()

    def initializeTreeview(self):
        self.raman_search_frame.initializeTreeview()

    def OnQuitApp(self):
        quit_app = quit_app_window.OnQuitApp(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
