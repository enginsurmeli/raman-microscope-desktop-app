import customtkinter
from PIL import Image
import os
from ctypes import *
import numpy as np


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
        button_size = (50, 50)

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=0)

        spectral_center_label = customtkinter.CTkLabel(
            self, text="Spectral Center (cm-1)")
        spectral_center_label.grid(
            row=0, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.spectral_center_entry = customtkinter.CTkEntry(
            self, width=entry_box_width, justify="center")
        self.spectral_center_entry.grid(
            row=0, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        integration_time_label = customtkinter.CTkLabel(
            self, text="Integration Time (s)")
        integration_time_label.grid(
            row=1, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.integration_time_entry = customtkinter.CTkEntry(
            self, width=entry_box_width, justify="center")
        self.integration_time_entry.grid(
            row=1, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        accumulations_label = customtkinter.CTkLabel(
            self, text="No. of accumulations")
        accumulations_label.grid(
            row=2, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.accumulations_entry = customtkinter.CTkEntry(
            self, width=entry_box_width, justify="center")
        self.accumulations_entry.grid(
            row=2, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        start_scan_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "laser_light.png")),
                                                 dark_image=Image.open(os.path.join(
                                                     icons_folder, "laser_dark.png")),
                                                 size=button_size)

        self.start_scan_button = customtkinter.CTkButton(
            self, text="Start\nScan", command=self.startRamanScan, width=button_size[0], height=button_size[1], image=start_scan_icon, compound="top")
        self.start_scan_button.grid(row=0, column=2, rowspan=3,
                                    padx=inner_frame_padding, pady=inner_frame_padding)

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

    def setScanParameters(self):
        # set integration time in  seconds, ranging from 1e-5 to 6e1
        integration_time = c_double(self.constrain(
            float(self.integration_time_entry.get())*1000, 1e-5, 6e1))
        self.spectrometer.tlccs_setIntegrationTime(
            self.ccs_handle, integration_time)

    def startRamanScan(self):
        self.setScanParameters()
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
        # TODO: Add sample name
        self.master.plotRamanData('', self.raman_shift, self.intensity)

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

    def updateSettings(self, spectral_center: str, integration_time: str, accumulations: str):
        self.spectral_center_entry.delete(0, "end")
        self.spectral_center_entry.insert(0, spectral_center)
        self.integration_time_entry.delete(0, "end")
        self.integration_time_entry.insert(0, integration_time)
        self.accumulations_entry.delete(0, "end")
        self.accumulations_entry.insert(0, accumulations)
