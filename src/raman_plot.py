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
        self.main_fig.subplots_adjust(
            left=figure_padding, bottom=figure_padding+0.02, right=1-figure_padding, top=1-figure_padding)

        self.main_canvas = FigureCanvasTkAgg(
            self.main_fig, master=self.plot_frame)
        self.main_canvas.draw()
        self.main_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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

        self.save_file_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Save", image=save_file_icon, command=self.saveFile, width=button_size[0], height=button_size[1])
        self.save_file_button.pack(side='left', expand=False, padx=inner_frame_padding,
                                   pady=inner_frame_padding)

        self.load_file_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Open", image=load_file_icon, command=self.loadFile, width=button_size[0], height=button_size[1])
        self.load_file_button.pack(side='left', expand=False, padx=inner_frame_padding,
                                   pady=inner_frame_padding)

        self.export_image_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Export\nImage", image=export_image_icon, command=self.exportGraphImage, width=button_size[0], height=button_size[1])
        self.export_image_button.pack(side='left', expand=False, padx=inner_frame_padding,
                                      pady=inner_frame_padding)

        self.camera_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Export\nCamera", image=camera_icon, command=self.exportCameraImage, width=button_size[0], height=button_size[1])
        self.camera_button.pack(side='left', expand=False, padx=inner_frame_padding,
                                pady=inner_frame_padding)

        separator1 = ttk.Separator(
            self.button_toolbar_frame, orient="vertical")
        separator1.pack(side='left', expand=False,
                        padx=inner_frame_padding, pady=inner_frame_padding)

        self.remove_baseline_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Remove\nBaseline", image=remove_baseline_icon, command=self.removeBaseline, width=button_size[0], height=button_size[1])
        self.remove_baseline_button.pack(side='left', expand=False, padx=inner_frame_padding,
                                         pady=inner_frame_padding)

        self.clear_plot_button = customtkinter.CTkButton(
            master=self.button_toolbar_frame, text="Clear", image=clear_plot_icon, command=self.clearPlot, width=button_size[0], height=button_size[1])
        self.clear_plot_button.pack(side='left', expand=False, padx=inner_frame_padding,
                                    pady=inner_frame_padding)

        self.toolbar = NavigationToolbar2Tk(
            self.main_canvas, self.button_toolbar_frame)
        unwanted_buttons = ["Subplots", "Save",
                            "Back", "Forward", "Home", "Pan", "Zoom"]
        for button in unwanted_buttons:
            self.toolbar._buttons[str(button)].pack_forget()
        self.toolbar.update()

        # Create span selector
        self.span = SpanSelector(self.span_plot, self.OnSpanSelect, "horizontal", useblit=True, props=dict(
            alpha=0.5, facecolor="tab:blue"), interactive=True, drag_from_anywhere=True, ignore_event_outside=False)

        # Initialize button states
        self.configureButtons(['save_file_button', 'export_image_button', 'camera_button',
                               'remove_baseline_button', 'clear_plot_button'], 'disabled')

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

    def loadFile(self):
        filepath = fd.askopenfilename(
            initialdir=self.save_folder, title="Select file", filetypes=(("all files", "*.*"), ("text files", "*.txt")))
        if filepath:
            self.clearPlot()
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
            self.main_canvas.draw_idle()

            self.span_xmin = self.raman_shift[0]
            self.span_xmax = self.raman_shift[-1]

            self.remove_baseline_button.configure(state='normal')
            self.master.configureButtons(
                'raman_search_frame', ['search_button'], 'normal')
            self.configureButtons(['save_file_button', 'export_image_button',
                                   'remove_baseline_button', 'clear_plot_button'], 'normal')

    def OnSpanSelect(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.raman_shift, (xmin, xmax))
        indmax = min(len(self.raman_shift) - 1, indmax)

        region_x = self.raman_shift[indmin:indmax]
        region_y = self.intensity[indmin:indmax]
        self.span_xmin = self.raman_shift[indmin]
        self.span_xmax = self.raman_shift[indmax]

        if len(region_x) >= 2:
            self.line_main_plot.set_data(region_x, region_y)
            self.main_plot.set_xlim(region_x[0], region_x[-1])
            self.main_plot.set_ylim(region_y.min(), region_y.max())
            self.main_fig.canvas.draw_idle()

    def removeBaseline(self):
        baseObj = BaselineRemoval(self.intensity.flatten())
        self.intensity = baseObj.ZhangFit()
        norm = np.sqrt(sum(self.intensity**2))
        self.intensity = self.intensity / norm
        self.line_main_plot.set_data(self.raman_shift, self.intensity)
        self.main_plot.set_ylim(self.intensity.min(), self.intensity.max())
        self.line_span_plot.set_data(self.raman_shift, self.intensity)
        self.span_plot.set_ylim(self.intensity.min(), self.intensity.max())
        self.main_canvas.draw_idle()

    def saveFile(self):
        save_filepath = fd.asksaveasfilename(
            initialdir=f"{self.save_folder}/", title="Select a file", filetypes=(("CSV files", ".csv"), ("Text files", ".txt")), defaultextension="*.*")
        if save_filepath:
            with open(save_filepath, 'w') as f:
                f.write(f"Sample name: {self.sample_name}\n")
                f.write("Raman Shift,Intensity\n")
                for i in range(len(self.raman_shift)):
                    f.write(f"{self.raman_shift[i]},{self.intensity[i]}\n")
                f.close()

    def exportGraphImage(self):
        save_filepath = fd.asksaveasfilename(
            initialdir=f"{self.save_folder}/", title="Select a file", filetypes=(("PNG files", ".png"), ("PDF files", ".pdf"), ("SVG files", ".svg"), ("EPS files", ".eps")), defaultextension="*.*")
        if save_filepath:
            # extent = self.main_plot.get_window_extent().transformed(
            #     self.main_fig.dpi_scale_trans.inverted())
            # plt.savefig(save_filepath, dpi=400, transparent=True,
            #                bbox_inches=extent.expanded(1.1, 1.1))
            # self.main_plot.savefig(save_filepath, dpi=400, transparent=True)
            self.main_fig.savefig(save_filepath, dpi=400, transparent=False,
                                  facecolor=self.main_fig.get_facecolor(), edgecolor='none')

    def exportCameraImage(self):
        self.master.exportCameraImage()

    def clearPlot(self):
        self.line_db_plot = {}
        self.main_plot.cla()
        self.span_plot.cla()
        self.main_plot.set_yticks([])
        self.span_plot.set_yticks([])
        self.span_plot.set_xticks([])
        self.main_fig.canvas.draw_idle()
        self.span_fig.canvas.draw_idle()

        self.configureButtons(
            ['save_file_button', 'export_image_button', 'remove_baseline_button'], 'disabled')
        self.master.configureButtons(
            'raman_search_frame', ['search_button'], 'disabled')

        self.master.initializeTreeview()

    def changeSaveFolder(self, save_folder):
        self.save_folder = save_folder

    def plotFromLibrary(self, db_filepath, db_filename: str, add: bool):
        if add:
            self.line_db_plot[db_filename], = self.main_plot.plot(
                [], [], label=db_filename)
            db_raman_shift, db_intensity = np.loadtxt(
                db_filepath, unpack=True, delimiter=',')
            self.line_db_plot[db_filename].set_data(
                db_raman_shift, db_intensity)
        else:
            self.line_db_plot[db_filename].remove()
        self.main_plot.legend()
        self.main_fig.canvas.draw_idle()

    def configureButtons(self, buttons: tuple, state: str):
        button_dict = {'save_file_button': self.save_file_button, 'load_file_button': self.load_file_button, 'export_image_button': self.export_image_button,
                       'camera_button': self.camera_button, 'remove_baseline_button': self.remove_baseline_button, 'clear_plot_button': self.clear_plot_button}
        for button in buttons:
            button_dict.get(button).configure(state=state)
