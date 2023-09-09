import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

import os

from BaselineRemoval import BaselineRemoval

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)  # type: ignore
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.widgets import SpanSelector
from matplotlib.backend_bases import key_press_handler

import numpy as np


class RamanPlot(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # self.grid_rowconfigure(0, weight=1)
        # self.grid_rowconfigure(1, weight=0)
        # self.grid_columnconfigure(0, weight=1)

        self.plot_frame = customtkinter.CTkFrame(self)
        self.plot_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.span_selector_frame = customtkinter.CTkFrame(self)
        self.span_selector_frame.pack(
            fill="both", expand=False, padx=10, pady=10)

    def changeTheme(self, color_palette):
        pass
