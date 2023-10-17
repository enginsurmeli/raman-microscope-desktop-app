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
                self.image_path, "app_logo.png"))
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

        settings_data = self.loadSettings()
        self.updateSettings(settings_data)

    def loadSettings(self):
        settings_data = {}
        jfile = None

        try:
            jfile = open('settings.json')
            settings_data = json.load(jfile)
        except FileNotFoundError as fnfe:
            pass
        if jfile:
            jfile.close()

        return settings_data

    def saveSettingsOnExit(self):
        settings_data = self.loadSettings()
        cnc_settings_data = self.cnc_buttons_frame.getSettingsData()
        spectrometer_settings_data = self.raman_scan_frame.getSettingsData()

        settings_data['last_y'] = cnc_settings_data.get('last_y')
        settings_data['last_z'] = cnc_settings_data.get('last_z')
        settings_data['last_cnc_state'] = cnc_settings_data.get(
            'last_cnc_state')
        settings_data['step_size'] = cnc_settings_data.get('step_size')
        settings_data['feed_rate'] = cnc_settings_data.get('feed_rate')
        settings_data['last_x'] = cnc_settings_data.get('last_x')

        settings_data['spectral_center'] = spectrometer_settings_data.get(
            'spectral_center')
        settings_data['integration_time'] = spectrometer_settings_data.get(
            'integration_time')
        settings_data['accumulations'] = spectrometer_settings_data.get(
            'accumulations')

        with open('settings.json', 'w') as jfile:
            json.dump(settings_data, jfile, indent=4)
            jfile.close()

    def updateSettings(self, settings_data: dict):
        self.settings_data = settings_data
        serial_line_ending = settings_data.get('lineending')
        baudrate = settings_data.get('baudrate')
        serial_port = settings_data.get('port')
        camera_index = settings_data.get('camera_index')
        appearance = settings_data.get('appearance')
        save_folder = settings_data.get('save_folder')
        step_size = settings_data.get('step_size')
        feed_rate = settings_data.get('feed_rate')
        spectral_center = settings_data.get('spectral_center')
        integration_time = settings_data.get('integration_time')
        accumulations = settings_data.get('accumulations')

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
        self.camera_view_frame.changeSaveFolder(save_folder=save_folder)

        # change cnc settings
        self.cnc_buttons_frame.updateSettings(step_size, feed_rate)

        # change spectrometer settings
        self.raman_scan_frame.updateSettings(
            spectral_center, integration_time, accumulations)

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

    def exportCameraImage(self):
        self.camera_view_frame.exportImage()

    def configureButtons(self, frame: str, buttons: tuple, state: str):
        frame_dict = {'cnc_buttons_frame': self.cnc_buttons_frame, 'raman_scan_frame': self.raman_scan_frame, 'serial_console_frame': self.serial_console_frame,
                      'raman_plot_frame': self.raman_plot_frame, 'camera_view_frame': self.camera_view_frame, 'raman_search_frame': self.raman_search_frame}
        frame_dict.get(frame).configureButtons(buttons, state)

    def plotRamanData(self, sample_name, raman_shift, intensity):
        self.raman_plot_frame.plotRamanData(
            sample_name, raman_shift, intensity)

    def plotFromRamanDB(self, db_filepath: str, db_filename: str, add: bool):
        self.raman_plot_frame.plotFromRamanDB(db_filepath, db_filename, add)

    def clearDBPlot(self):
        self.raman_plot_frame.clearDBPlot()

    def getSpanSelection(self):
        return self.raman_plot_frame.getSpanSelection()

    def disconnectDevices(self):
        self.serial_console_frame.closePort()
        self.camera_view_frame.closeCamera()
        self.raman_scan_frame.disconnectSpectrometer()

    def OnQuitApp(self):
        quit_app = quit_app_window.OnQuitApp(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
