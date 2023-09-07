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
        
        # self.label1 = customtkinter.CTkLabel(self, text="Raman Plot")
        # self.label1.grid(row=0, column=0, sticky="nsew")
        
        # self.label2 = customtkinter.CTkLabel(self, text="Span Selector")
        # self.label2.grid(row=1, column=0, sticky="nsew")
        
        self.raman_plot_frame = customtkinter.CTkFrame(self)
        self.raman_plot_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.span_selector_frame = customtkinter.CTkFrame(self)
        self.span_selector_frame.pack(fill="both", expand=False, padx=10, pady=10)
        
        self.label1 = customtkinter.CTkLabel(self.raman_plot_frame, text="Raman Plot")
        self.label1.pack(fill="both", expand=True)
        
        self.label2 = customtkinter.CTkLabel(self.span_selector_frame, text="Span Selector")
        self.label2.pack(fill="both", expand=True)
