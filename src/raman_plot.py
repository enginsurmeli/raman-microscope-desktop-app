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
        main_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.span_fig = Figure(figsize=(5, 1), dpi=100)
        self.span_plot = self.span_fig.add_subplot(111)
        self.span_plot.plot([1, 2, 3, 4, 5], [10, 20, 30, 40, 50])
        
        span_canvas = FigureCanvasTkAgg(self.span_fig, master=self.span_selector_frame)
        span_canvas.draw()
        self.toolbar = NavigationToolbar2Tk(main_canvas, self.span_selector_frame)
        unwanted_buttons = ["Subplots", "Save", "Back", "Forward", "Home", "Pan", "Zoom"]
        for button in unwanted_buttons:
            self.toolbar._buttons[str(button)].pack_forget()
        self.toolbar.update()
        span_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def changeTheme(self, color_palette):
        self.main_fig.set_facecolor(color_palette[0])
        self.main_plot.set_facecolor(color_palette[0])
        self.main_plot.tick_params(axis='x', colors=color_palette[3])
        self.main_plot.xaxis.label.set_color(color_palette[3])
        self.main_plot.spines['bottom'].set_color(color_palette[3])
        self.main_plot.spines['top'].set_color(color_palette[3])
        self.main_plot.spines['left'].set_color(color_palette[3])
        self.main_plot.spines['right'].set_color(color_palette[3])
        self.main_plot.set_yticks([])
        
        self.span_fig.set_facecolor(color_palette[0])
        self.span_plot.set_facecolor(color_palette[0])
        self.span_plot.tick_params(axis='x', colors=color_palette[3])
        self.span_plot.xaxis.label.set_color(color_palette[3])
        self.span_plot.spines['bottom'].set_color(color_palette[3])
        self.span_plot.spines['top'].set_color(color_palette[3])
        self.span_plot.spines['left'].set_color(color_palette[3])
        self.span_plot.spines['right'].set_color(color_palette[3])
        self.span_plot.set_yticks([])
        self.span_plot.set_xticks([])
        
        self.toolbar.config(background=color_palette[0])
        self.toolbar.winfo_children()[-2].config(background=color_palette[0])
        self.toolbar._message_label.config(
            background=color_palette[0], foreground=color_palette[3])
        self.toolbar.update()
