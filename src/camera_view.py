import customtkinter
import tkinter as tk

import cv2
from pygrabber.dshow_graph import FilterGraph
from PIL import Image, ImageTk


class CameraView(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.connection_active = False
        self.previous_camera_index = -1

    def connect_camera(self, camera_index: int = 0):
        if self.previous_camera_index == camera_index:
            return

        if self.connection_active:  # close camera if already connected
            self.closeCamera()

        self.vid = cv2.VideoCapture(camera_index)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", camera_index)
        self.connection_active = True
        self.previous_camera_index = camera_index

        self.canvas = tk.Canvas(
            self, highlightthickness=0, width=480, height=360)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.stream()  # start streaming

    def stream(self):
        # Get a frame from the video source
        return_value, frame = self.get_frame()

        if return_value:
            try:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

            except BaseException:
                import sys
                print(sys.exc_info()[0])
                import traceback
                print(traceback.format_exc())
            finally:
                pass

        fps = 30
        delay = round(1000/fps)
        self.after(delay, self.stream)

    def get_frame(self):
        if not self.vid.isOpened():
            return (return_value, None)

        return_value, frame = self.vid.read()
        dim = (self.canvas.winfo_width(), self.canvas.winfo_height())
        # fit frame to canvas
        frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        # flip frame horizontally
        frame = cv2.flip(frame, 1)
        if return_value:
            # Return a boolean success flag and the current frame converted to BGR
            return (return_value, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        else:
            return (return_value, None)

    def closeCamera(self):
        if self.vid.isOpened():
            self.canvas.destroy()
            self.vid.release()
            self.connection_active = False

    def exportImage(self):
        pass
