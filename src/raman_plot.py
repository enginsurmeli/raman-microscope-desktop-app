import customtkinter
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd

from PIL import Image

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

        self.master = master
        icons_folder = os.path.join(os.getcwd(), 'src', 'icons')

        inner_frame_padding = 5
        figure_padding = 0.02
        button_size = (30, 30)

        self.plot_frame = customtkinter.CTkFrame(self)
        self.plot_frame.pack(fill="both", expand=True,
                             padx=inner_frame_padding, pady=inner_frame_padding)

        self.span_selector_frame = customtkinter.CTkFrame(self)
        self.span_selector_frame.pack(
            fill="both", expand=False, padx=inner_frame_padding, pady=inner_frame_padding)

        self.button_toolbar_frame = customtkinter.CTkFrame(self)
        self.button_toolbar_frame.pack(fill="both", expand=False,
                                       padx=inner_frame_padding*4, pady=inner_frame_padding)

        self.main_fig = Figure(figsize=(5, 4), dpi=100)
        self.main_plot = self.main_fig.add_subplot(111)
        self.line_main_plot = self.main_plot.plot([], [])
        self.line_db_plot = {}
        self.main_fig.subplots_adjust(
            left=figure_padding, bottom=figure_padding+0.02, right=1-figure_padding, top=1-figure_padding)

        main_canvas = FigureCanvasTkAgg(self.main_fig, master=self.plot_frame)
        main_canvas.draw()
        main_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.span_fig = Figure(figsize=(5, 1), dpi=100)
        self.span_plot = self.span_fig.add_subplot(111)
        self.span_fig.subplots_adjust(
            left=figure_padding, bottom=figure_padding, right=1-figure_padding, top=1-figure_padding)

        span_canvas = FigureCanvasTkAgg(
            self.span_fig, master=self.span_selector_frame)
        span_canvas.draw()
        span_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        save_file_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "save_light.png")),
                                                dark_image=Image.open(os.path.join(
                                                    icons_folder, "save_dark.png")),
                                                size=button_size)
        export_image_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "export_image_light.png")),
                                                   dark_image=Image.open(os.path.join(
                                                       icons_folder, "export_image_dark.png")),
                                                   size=button_size)
        load_file_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "open_light.png")),
                                                dark_image=Image.open(os.path.join(
                                                    icons_folder, "open_dark.png")),
                                                size=button_size)
        camera_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "camera_light.png")),
                                             dark_image=Image.open(os.path.join(
                                                 icons_folder, "camera_dark.png")),
                                             size=button_size)
        remove_baseline_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "baseline_light.png")),
                                                      dark_image=Image.open(os.path.join(
                                                          icons_folder, "baseline_dark.png")),
                                                      size=button_size)
        clear_plot_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "clear_plot_light.png")),
                                                 dark_image=Image.open(os.path.join(
                                                     icons_folder, "clear_plot_dark.png")),
                                                 size=button_size)

        save_file_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Save", image=save_file_icon, command=self.exportCSV, width=button_size[0], height=button_size[1])
        save_file_button.pack(side='left', expand=False, padx=inner_frame_padding,
                              pady=inner_frame_padding)

        load_file_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Open", image=load_file_icon, command=self.LoadSpectrumFile, width=button_size[0], height=button_size[1])
        load_file_button.pack(side='left', expand=False, padx=inner_frame_padding,
                              pady=inner_frame_padding)

        export_image_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Export\nGraph", image=export_image_icon, command=self.exportPNG, width=button_size[0], height=button_size[1])
        export_image_button.pack(side='left', expand=False, padx=inner_frame_padding,
                                 pady=inner_frame_padding)

        camera_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Export\nCamera", image=camera_icon, command=self.exportCameraImage, width=button_size[0], height=button_size[1])
        camera_button.pack(side='left', expand=False, padx=inner_frame_padding,
                           pady=inner_frame_padding)

        separator1 = ttk.Separator(
            self.button_toolbar_frame, orient="vertical")
        separator1.pack(side='left', expand=False,
                        padx=inner_frame_padding, pady=inner_frame_padding)

        remove_baseline_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Remove\nBaseline", image=remove_baseline_icon, command=self.removeBaseline, width=button_size[0], height=button_size[1])
        remove_baseline_button.pack(side='left', expand=False, padx=inner_frame_padding,
                                    pady=inner_frame_padding)

        clear_plot_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Clear", image=clear_plot_icon, command=self.clearPlot, width=button_size[0], height=button_size[1])
        clear_plot_button.pack(side='left', expand=False, padx=inner_frame_padding,
                                    pady=inner_frame_padding)

        self.toolbar = NavigationToolbar2Tk(
            main_canvas, self.button_toolbar_frame)
        unwanted_buttons = ["Subplots", "Save",
                            "Back", "Forward", "Home", "Pan", "Zoom"]
        for button in unwanted_buttons:
            self.toolbar._buttons[str(button)].pack_forget()
        self.toolbar.update()

        # Create span selector
        self.span = SpanSelector(self.span_plot, self.OnSpanSelect, "horizontal", useblit=True, props=dict(
            alpha=0.5, facecolor="tab:blue"), interactive=True, drag_from_anywhere=True, ignore_event_outside=False)

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

        self.toolbar.config(background=color_palette[4])
        self.toolbar.winfo_children()[-2].config(background=color_palette[4])
        self.toolbar._message_label.config(
            background=color_palette[4], foreground=color_palette[3])

    def LoadSpectrumFile(self):
        filepath = fd.askopenfilename(
            initialdir=self.save_folder, title="Select file", filetypes=(("all files", "*.*"), ("text files", "*.txt")))
        if filepath:  # if user wants to load specimen spectrum, open a file dialog
            # self.search_button.configure(state='disabled')
            # self.remove_baseline_button.configure(state='disabled')
            self.main_plot.cla()
            self.span_plot.cla()
            self.main_plot.set_yticks([])
            self.span_plot.set_yticks([])
            self.span_plot.set_xticks([])
            self.main_fig.canvas.draw_idle()
            # for child in self.raman_db_treeview.get_children():
            #     # self.raman_db_treeview.set(child, column=0, value='--')
            #     self.raman_db_treeview.delete(child)

            try:
                self.raman_shift, self.intensity = np.loadtxt(
                    filepath, unpack=True)
            except:
                self.raman_shift, self.intensity = np.loadtxt(
                    filepath, unpack=True, delimiter=',')

            self.sample_name = filepath.split('/')[-1].replace('.txt', '')
            norm = np.sqrt(sum(self.intensity**2))
            self.intensity = self.intensity / norm
            self.line_main_plot, = self.main_plot.plot(
                [], [], label=self.sample_name)
            self.line_main_plot.set_data(self.raman_shift, self.intensity)
            self.main_plot.set_xlim(
                self.raman_shift[0], self.raman_shift[-1])
            self.main_plot.set_ylim(
                self.intensity.min(), self.intensity.max())

            self.line_span_plot, = self.span_plot.plot([], [])
            self.line_span_plot.set_data(
                self.raman_shift, self.intensity)
            self.span_plot.set_xlim(
                self.raman_shift[0], self.raman_shift[-1])
            self.span_plot.set_ylim(
                self.intensity.min(), self.intensity.max())
            self.main_plot.set_yticks([])
            self.span_plot.set_yticks([])
            self.span_plot.set_xticks([])
            self.main_plot.legend()
            self.main_plot.canvas.draw_idle()
            # self.search_button.configure(state='normal')
            # self.remove_baseline_button.configure(state='normal')

            self.span_xmin = self.raman_shift[0]
            self.span_xmax = self.raman_shift[-1]

            self.master.initializeTreeview()

    def OnSpanSelect(self, xmin, xmax):
        pass

    def removeBaseline(self):
        pass

    def exportCSV(self):
        pass

    def exportPNG(self):
        pass

    def exportCameraImage(self):
        pass

    def clearPlot(self):
        pass

    def changeSaveFolder(self, save_folder):
        self.save_folder = save_folder
