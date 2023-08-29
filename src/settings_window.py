import customtkinter
import serial.tools.list_ports
import json
from pygrabber.dshow_graph import FilterGraph
import tkinter.ttk as ttk


class SettingsWindow(customtkinter.CTkToplevel):
    def __init__(self, master, settings_data: dict):
        super().__init__(master)

        self.master = master
        self.settings_data = settings_data

        app_window_width = master.winfo_width()
        app_window_height = master.winfo_height()
        app_window_x = master.winfo_x()
        app_window_y = master.winfo_y()
        settings_window_width = 600
        settings_window_height = 240
        self.geometry(
            f"{settings_window_width}x{settings_window_height}+{app_window_x+app_window_width//2-settings_window_width//2}+{app_window_y+app_window_height//2-settings_window_height//2}")
        self.resizable(False, False)
        self.title("Settings")
        self.deiconify()
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
        self.ports_list = sorted([p[0] for p in myports])
        self.serial_ports_optionmenu = customtkinter.CTkOptionMenu(
            self.settings_frame, values=self.ports_list)
        self.serial_ports_optionmenu.grid(row=0, column=1, padx=10, pady=10)

        # create a list of baud rates
        baud_rates = ["9600", "19200", "38400", "57600", "115200"]
        self.baud_rates_optionmenu = customtkinter.CTkOptionMenu(
            self.settings_frame, values=baud_rates)
        self.baud_rates_optionmenu.grid(row=0, column=2, padx=10, pady=10)

        # create a list of line endings
        line_endings = ["None", "CR", "LF", "Both CR&LF"]
        self.line_endings_optionmenu = customtkinter.CTkOptionMenu(
            self.settings_frame, values=line_endings)
        self.line_endings_optionmenu.grid(row=0, column=3, padx=10, pady=10)

        # get a list of available video devices
        self.graph = FilterGraph()

        # fill optionmenu with video devices
        self.camera_list = self.graph.get_input_devices()
        self.camera_optionmenu = customtkinter.CTkOptionMenu(
            self.settings_frame, values=self.camera_list, dynamic_resizing=False)
        self.camera_optionmenu.grid(row=2, column=1, padx=10, pady=10)

        # create a list of appearance modes and accent colors
        self.appearance_optionmenu = customtkinter.CTkOptionMenu(
            self.settings_frame, values=["Light", "Dark", "System"])
        self.appearance_optionmenu.grid(row=4, column=1, padx=10, pady=10)

        # self.accent_color_option = customtkinter.CTkOptionMenu(
        #     self.settings_frame, values=["blue", "green", "dark-blue"])
        # self.accent_color_option.grid(row=4, column=2, padx=10, pady=10)

        self.setCurrentSettings()

    def setCurrentSettings(self):
        camera_index = self.settings_data.get('camera_index')
        self.serial_ports_optionmenu.set(self.settings_data.get('port'))
        self.baud_rates_optionmenu.set(self.settings_data.get('baudrate'))
        self.line_endings_optionmenu.set(self.settings_data.get('lineending'))
        self.camera_optionmenu.set(self.camera_list[camera_index])
        self.appearance_optionmenu.set(self.settings_data.get('appearance'))

    # TODO: implement this, refresh available serial ports and cameras every 1 second
    def refreshPorts(self):
        pass

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def apply_settings(self):

        # get serial port, baud rate and line ending
        serial_port = self.serial_ports_optionmenu.get()
        baud_rate = self.baud_rates_optionmenu.get()
        line_ending = self.line_endings_optionmenu.get()

        # get camera index
        camera = self.camera_optionmenu.get()
        for i, device in enumerate(self.camera_list):
            if device == camera:
                camera_index = i

        # change appearance mode
        appearance = self.appearance_optionmenu.get()
        self.change_appearance_mode_event(appearance)

        # save settings to json file
        settings_data = {}
        settings_data['lineending'] = line_ending
        settings_data['baudrate'] = baud_rate
        settings_data['port'] = serial_port
        settings_data['portlist'] = self.ports_list
        settings_data['camera_index'] = camera_index
        settings_data['cameralist'] = self.camera_list
        settings_data['appearance'] = appearance
        with open('settings.json', 'w') as jfile:
            json.dump(settings_data, jfile, indent=4)
            jfile.close()
        self.master.updateSettings(settings_data)
        self.destroy()
