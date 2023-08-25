import customtkinter

import cv2
from pygrabber.dshow_graph import FilterGraph


class CameraView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
