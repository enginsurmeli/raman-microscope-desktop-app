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

        self.main_fig = Figure(figsize=(5, 4), dpi=100)
        self.main_plot = self.main_fig.add_subplot(111)
        self.main_plot.plot([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])

        main_canvas = FigureCanvasTkAgg(self.main_fig, master=self.plot_frame)
        main_canvas.draw()

        # main_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        toolbar = NavigationToolbar2Tk(main_canvas, self.plot_frame)
        toolbar.update()
        main_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.span_fig = Figure(figsize=(5, 1), dpi=100)
        self.span_plot = self.span_fig.add_subplot(111)
        self.span_plot.plot([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
        
        span_canvas = FigureCanvasTkAgg(self.span_fig, master=self.span_selector_frame)
        span_canvas.draw()
        span_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def changeTheme(self, color_palette):
        pass
