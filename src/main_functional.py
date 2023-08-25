import sys
import os
from PIL import Image, ImageTk

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import customtkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)  # type: ignore
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.widgets import SpanSelector
from matplotlib.backend_bases import key_press_handler

import numpy as np

import random
import serial
import serial.tools.list_ports as list_ports
import json

import cv2
from pygrabber.dshow_graph import FilterGraph


def ApplySettings():
    pass


def OnQuitApp():
    quit_app_window = customtkinter.CTkToplevel(app)
    quit_app_window.geometry(
        f"320x100+{app.winfo_x()+app.winfo_width()//2-160}+{app.winfo_y()+app.winfo_height()//2-50}")
    quit_app_window.title("Quit Application")
    quit_app_window.resizable(False, False)
    quit_app_window.deiconify()
    quit_app_window.grab_set()

    label = customtkinter.CTkLabel(
        quit_app_window, text="Are you sure you want to quit?")
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
    yes_button = customtkinter.CTkButton(
        quit_app_window, text="Yes", command=_quit)
    yes_button.grid(row=1, column=0, padx=10, pady=10)
    no_button = customtkinter.CTkButton(
        quit_app_window, text="No", command=quit_app_window.destroy)
    no_button.grid(row=1, column=1, padx=10, pady=10)


def _quit():
    app.quit()
    app.destroy()


app = customtkinter.CTk()
app.title("LST Raman Microscope Scanner")
app.protocol("WM_DELETE_WINDOW", OnQuitApp)

app_window_width = 1280
app_window_height = 720
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
app.geometry(
    f"{app_window_width}x{app_window_height}+{int(screen_width/2-app_window_width/2)}+{int(screen_height/2-app_window_height/2)}")
app.minsize(app_window_width, app_window_height)
app.grab_set()

app.mainloop()
