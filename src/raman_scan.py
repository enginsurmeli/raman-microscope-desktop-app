from typing import Optional, Tuple, Union
import customtkinter
from PIL import Image
import os
from ctypes import *
import numpy as np
from datetime import datetime


class RamanScan(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        icons_folder = os.path.join(os.getcwd(), 'src', 'icons')
        dll_folder = 'thorlabs_lib'
        dll_filepath = os.path.join(os.path.dirname(
            __file__), '..', dll_folder, 'TLCCS_64.dll')
        self.spectrometer = cdll.LoadLibrary(dll_filepath)

        inner_frame_padding = 4
        entry_box_width = 75
        button_size = (30, 30)

        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        spectral_center_label = customtkinter.CTkLabel(
            self, text="Spectral Center (cm⁻¹)")
        spectral_center_label.grid(
            row=0, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.spectral_center_entry = Spinbox(self, step_size=1, min_value=-3000, max_value=3000,
                                             decimal_places=0)
        self.spectral_center_entry.grid(
            row=0, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        integration_time_label = customtkinter.CTkLabel(
            self, text="Integration Time (s)")
        integration_time_label.grid(
            row=1, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.integration_time_entry = Spinbox(self, step_size=1, min_value=1, max_value=1000,
                                              decimal_places=0)
        self.integration_time_entry.grid(
            row=1, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        accumulations_label = customtkinter.CTkLabel(
            self, text="No. of accumulations")
        accumulations_label.grid(
            row=2, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.accumulations_entry = Spinbox(self, step_size=1, min_value=1, max_value=1000,
                                           decimal_places=0)
        self.accumulations_entry.grid(
            row=2, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        start_scan_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "laser_light.png")),
                                                 dark_image=Image.open(os.path.join(
                                                     icons_folder, "laser_dark.png")),
                                                 size=button_size)

        self.start_scan_button = customtkinter.CTkButton(
            self, text="Start Scan", command=self.startRamanScan, width=button_size[0], height=button_size[1], image=start_scan_icon)
        self.start_scan_button.grid(row=3, column=0, columnspan=2,
                                    padx=inner_frame_padding, pady=inner_frame_padding, sticky="nsew")

        self.raman_shift = []
        self.intensity = []

        self.configureButtons(['start_scan_button'], 'disabled')
        self.is_connected = False

        self.connectSpectrometer()

    def connectSpectrometer(self):
        # The resource name has this format: USB0::0x1313::<product ID>::<serial number>::RAW
        #
        # Product IDs are:
        # 0x8081   // CCS100 Compact Spectrometer
        # 0x8083   // CCS125 Special Spectrometer
        # 0x8085   // CCS150 UV Spectrometer
        # 0x8087   // CCS175 NIR Spectrometer
        # 0x8089   // CCS200 UV-NIR Spectrometer
        #
        # The serial number is printed on the CCS spectrometer.
        #
        # E.g.: "USB0::0x1313::0x8081::M00822009::RAW" for a CCS100 with serial number M00822009

        serial_number = "M00822009"
        product_id = "0x8081"
        coding = 'utf-8'
        device_address = bytes(
            f"USB0::0x1313::{product_id}::{serial_number}::RAW", coding)
        self.ccs_handle = c_int(0)
        connect_spectrometer = self.spectrometer.tlccs_init(
            device_address, 1, 1, byref(self.ccs_handle))

        self.is_connected = True if connect_spectrometer == 0 else False

        if self.is_connected:
            self.configureButtons(['start_scan_button'], 'normal')
        else:
            self.after(1000, self.connectSpectrometer)

    def disconnectSpectrometer(self):
        self.configureButtons(['start_scan_button'], 'disabled')
        self.is_connected = False
        self.spectrometer.tlccs_close(self.ccs_handle)

    def setIntegrationTime(self):
        # set integration time in  seconds, ranging from 1e-5 to 5e1
        integration_time = c_double(self.constrain(
            float(self.integration_time_entry.get()), 1e-5, 5e1))
        self.spectrometer.tlccs_setIntegrationTime(
            self.ccs_handle, integration_time)

    def startRamanScan(self):
        self.setIntegrationTime()
        self.spectrometer.tlccs_startScan(self.ccs_handle)

        wavelengths = (c_double*3648)()

        self.spectrometer.tlccs_getWavelengthData(self.ccs_handle, 0, byref(
            wavelengths), c_void_p(None), c_void_p(None))

        # retrieve data
        data_array = (c_double*3648)()
        self.spectrometer.tlccs_getScanData(self.ccs_handle, byref(data_array))

        raman_shift_nm = np.ndarray(
            shape=(3648,), dtype=float, buffer=wavelengths)
        raman_shift_inverse_cm = 1e7*(1/532 - 1/raman_shift_nm)
        self.raman_shift = raman_shift_inverse_cm
        self.intensity = np.ndarray(
            shape=(3648,), dtype=float, buffer=data_array)

        self.sendDataToPlot()

    def sendDataToPlot(self):
        datetime_string = datetime.now().strftime("%Y-%m-%d_%H-%M")
        sample_name = f"Sample_{datetime_string}"
        self.master.plotRamanData(
            sample_name, self.raman_shift, self.intensity)

    def configureButtons(self, buttons: tuple, state: str):
        button_dict = {'start_scan_button': self.start_scan_button, 'spectral_center_entry': self.spectral_center_entry,
                       'integration_time_entry': self.integration_time_entry, 'accumulations_entry': self.accumulations_entry}
        for button in buttons:
            button_dict.get(button).configure(state=state)

    def constrain(self, value, min_value, max_value):
        return min(max(value, min_value), max_value)

    def getSettingsData(self):
        settings_data = {}
        settings_data['spectral_center'] = self.spectral_center_entry.get()
        settings_data['integration_time'] = self.integration_time_entry.get()
        settings_data['accumulations'] = self.accumulations_entry.get()
        return settings_data

    def updateSettings(self, spectral_center: float, integration_time: float, accumulations: float):
        self.spectral_center_entry.set(spectral_center)
        self.integration_time_entry.set(integration_time)
        self.accumulations_entry.set(accumulations)


class Spinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                 step_size: float = 1,
                 decimal_places: int = 0,
                 min_value, max_value,
                 **kwargs):
        super().__init__(*args, **kwargs)

        self.step_size = step_size
        self.min_value = min_value
        self.max_value = max_value
        self.decimal_places = decimal_places

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        validation = self.register(self.only_numbers)

        self.entrybox = customtkinter.CTkEntry(
            self, width=50, border_width=0, validate="key", validatecommand=(validation, '%P'))
        self.entrybox.grid(row=0, column=1, columnspan=1,
                           padx=3, pady=3, sticky="nsew")

        entrybox_height = self.entrybox.winfo_reqheight() - 2

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=entrybox_height, height=entrybox_height,
                                                       command=lambda: self.increment_callback('subtract'))
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.add_button = customtkinter.CTkButton(self, text="+", width=entrybox_height, height=entrybox_height,
                                                  command=lambda: self.increment_callback('add'))
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entrybox.insert(0, "0")
        # Bind all elements on mousewheel and keyboard events
        self.entrybox.bind("<MouseWheel>", self.on_mouse_wheel)
        self.subtract_button.bind("<MouseWheel>", self.on_mouse_wheel)
        self.add_button.bind("<MouseWheel>", self.on_mouse_wheel)
        self.bind("<MouseWheel>", self.on_mouse_wheel)

        self.entrybox.bind("<Up>", lambda e: self.increment_callback('add'))
        self.entrybox.bind(
            "<Down>", lambda e: self.increment_callback('subtract'))
        self.entrybox.bind("<FocusOut>", self.focusOutEvent)
        self.entrybox.bind("<Return>", lambda event: self.focus_set())

    def increment_callback(self, operation: str = "add"):
        try:
            if operation == "add":
                value = float(self.entrybox.get()) + self.step_size
            if operation == "subtract":
                value = float(self.entrybox.get()) - self.step_size
            value = self.constrain(value, self.min_value, self.max_value)
            self.set(value)
        except ValueError:
            return

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.increment_callback('add')
        else:
            self.increment_callback('subtract')

    # def set(self, value: float):
    #     self.entrybox.delete(0, "end")
    #     str_value = f"{value:.{self.decimal_places}}"
    #     self.entrybox.insert(0, str_value)

    def set(self, value):
        self.entrybox.delete(0, "end")
        if isinstance(value, (int, float)):
            # Format the value explicitly without scientific notation
            str_value = "{:.{}f}".format(value, self.decimal_places)
            self.entrybox.insert(0, str_value)
        else:
            # Handle non-numeric values (maybe display an error message?)
            print("Error: Value must be numeric")

    def only_numbers(self, char):
        def is_float(char):
            try:
                float(char)
                return True
            except ValueError:
                return False

        # Validate true for only numbers
        if (is_float(char) or char == ""):
            return True
        else:
            return False

    def constrain(self, value, min_value, max_value):
        if value < min_value:
            return min_value
        elif value > max_value:
            return max_value
        else:
            return value

    def focusOutEvent(self, event):
        self.set(self.constrain(float(self.entrybox.get()),
                 self.min_value, self.max_value))

    def get(self):
        return self.entrybox.get()
