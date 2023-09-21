import customtkinter
from PIL import Image
import os


class RamanScan(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        icons_folder = os.path.join(os.getcwd(), 'src', 'icons')

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

        accumulation_label = customtkinter.CTkLabel(
            self, text="No. of accumulations")
        accumulation_label.grid(
            row=2, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.accumulation_entry = customtkinter.CTkEntry(
            self, width=entry_box_width, justify="center")
        self.accumulation_entry.grid(
            row=2, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        start_scan_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "laser_light.png")),
                                                 dark_image=Image.open(os.path.join(
                                                     icons_folder, "laser_dark.png")),
                                                 size=button_size)

        self.start_scan_button = customtkinter.CTkButton(
            self, text="Start\nScan", command=self.startRamanScan, width=button_size[0], height=button_size[1], image=start_scan_icon, compound="top")
        self.start_scan_button.grid(row=0, column=2, rowspan=3,
                                    padx=inner_frame_padding, pady=inner_frame_padding)

        self.configureButtons(['start_scan_button'], 'disabled')

    def configureButtons(self, buttons: tuple, state: str):
        button_dict = {'start_scan_button': self.start_scan_button}
        for button in buttons:
            button_dict.get(button).configure(state=state)

    def startRamanScan(self):
        print("start raman scan")
