import customtkinter

import cv2
from pygrabber.dshow_graph import FilterGraph


class CameraView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.label1 = customtkinter.CTkLabel(self, text="Camera View")
        self.label1.pack(fill="both", expand=True)
