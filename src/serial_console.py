import customtkinter
from PIL import Image

import os

import serial
import serial.tools.list_ports as list_ports


class SerialConsole(customtkinter.CTkFrame):
    def __init__(self, master, serial_port=None, baudrate=None, line_ending=None):
        super().__init__(master)

        self.master = master

        icons_folder = os.path.join(os.getcwd(), 'src', 'icons')
        send_button_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "send_button_light.png")),
                                                  dark_image=Image.open(os.path.join(
                                                      icons_folder, "send_button_dark.png")),
                                                  size=(20, 20))
        clear_button_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "clear_button_light.png")),
                                                   dark_image=Image.open(os.path.join(
                                                       icons_folder, "clear_button_dark.png")),
                                                   size=(20, 20))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1, 2), weight=0)

        self.rx_textbox = customtkinter.CTkTextbox(
            self, bg_color='#343638', state="disabled", wrap="word", border_width=5, corner_radius=0)
        self.rx_textbox.grid(row=0, column=0, columnspan=3,
                             padx=5, pady=5, sticky="nsew")
        self.rx_textbox.insert('0.0', "RX: \n")

        self.tx_entrybox = customtkinter.CTkEntry(self)
        self.tx_entrybox.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.clear_button = customtkinter.CTkButton(
            self, text="", command=self.clear, width=5, height=5, image=clear_button_icon)
        self.clear_button.grid(row=1, column=1, padx=2.5, pady=5)

        self.send_button = customtkinter.CTkButton(
            self, text="", command=self.send, width=5, height=5, image=send_button_icon)
        self.send_button.grid(row=1, column=2, padx=5, pady=5)

    def clear(self):
        self.rx_textbox.configure(state="normal")
        self.rx_textbox.delete("0.0", 'end')
        self.rx_textbox.configure(state="disabled")

    def send(self, event=None):
        tx_text = self.tx_entrybox.get()
        if tx_text != "":
            self.rx_textbox.configure(state="normal")
            self.rx_textbox.insert('end', tx_text + "\n")
            self.rx_textbox.configure(state="disabled")
            self.tx_entrybox.delete(0, 'end')

    def disableSending(self):
        self.send_button.configure(state="disabled")
        self.tx_entrybox.unbind('<Return>')

    def enableSending(self):
        self.send_button.configure(state="normal")
        self.tx_entrybox.bind('<Return>', self.send)
