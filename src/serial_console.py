import customtkinter

import serial
import serial.tools.list_ports as list_ports


class SerialConsole(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
