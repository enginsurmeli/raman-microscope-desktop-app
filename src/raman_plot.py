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
from matplotlib import gridspec

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

        self.button_toolbar_frame = customtkinter.CTkFrame(self)
        self.button_toolbar_frame.pack(fill="both", expand=False,
                                       padx=inner_frame_padding*4, pady=inner_frame_padding)

        self.main_fig = Figure(figsize=(5, 5), dpi=100)
        spec = gridspec.GridSpec(
            ncols=1, nrows=2, figure=self.main_fig, height_ratios=[6, 1], wspace=0, hspace=0.075)
        self.main_ax = self.main_fig.add_subplot(spec[0])
        self.span_ax = self.main_fig.add_subplot(spec[1])
        self.line_main_plot, = self.main_ax.plot([], [])
        self.main_fig.subplots_adjust(
            left=figure_padding, bottom=figure_padding, right=1-figure_padding, top=1-figure_padding)

        self.main_canvas = FigureCanvasTkAgg(
            self.main_fig, master=self.plot_frame)
        self.main_canvas.draw()
        self.main_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

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

        # Create a navigation toolbar
        self.toolbar = NavigationToolbar2Tk(
            self.main_canvas, self.button_toolbar_frame)
        unwanted_buttons = ["Subplots", "Save",
                            "Back", "Forward", "Home", "Pan", "Zoom"]
        for button in unwanted_buttons:
            self.toolbar._buttons[str(button)].pack_forget()
        self.toolbar.update()

        # Create span selector
        self.span = SpanSelector(self.span_ax, self.OnSpanSelect, "horizontal", useblit=True, props=dict(
            alpha=0.5, facecolor="tab:blue"), interactive=True, drag_from_anywhere=True, ignore_event_outside=False)

        # Initialize button states
        self.configureButtons(['save_file_button', 'export_image_button', 'camera_button',
                               'remove_baseline_button', 'clear_plot_button'], 'disabled')

        self.line_db_plot = {}

    def changeTheme(self, color_palette):
        self.main_fig.set_facecolor(color_palette[0])
        self.main_ax.set_facecolor(color_palette[0])
        self.main_ax.tick_params(axis='x', colors=color_palette[3])
        self.main_ax.xaxis.label.set_color(color_palette[3])
        self.main_ax.spines['bottom'].set_color(color_palette[3])
        self.main_ax.spines['top'].set_color(color_palette[3])
        self.main_ax.spines['left'].set_color(color_palette[3])
        self.main_ax.spines['right'].set_color(color_palette[3])
        self.main_ax.set_yticks([])

        self.span_ax.set_facecolor(color_palette[0])
        self.span_ax.tick_params(axis='x', colors=color_palette[3])
        self.span_ax.xaxis.label.set_color(color_palette[3])
        self.span_ax.spines['bottom'].set_color(color_palette[3])
        self.span_ax.spines['top'].set_color(color_palette[3])
        self.span_ax.spines['left'].set_color(color_palette[3])
        self.span_ax.spines['right'].set_color(color_palette[3])
        self.span_ax.set_yticks([])
        self.span_ax.set_xticks([])

        self.toolbar.config(background=color_palette[4])
        self.toolbar.winfo_children()[-2].config(background=color_palette[4])
        self.toolbar._message_label.config(
            background=color_palette[4], foreground=color_palette[3])

        self.main_fig.canvas.draw_idle()

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
            self.plotSample(self.sample_name, self.raman_shift, self.intensity)

    def OnSpanSelect(self, xmin, xmax):
        indmin, indmax = np.searchsorted(self.raman_shift, (xmin, xmax))
        indmax = min(len(self.raman_shift) - 1, indmax)

        self.span_x = self.raman_shift[indmin:indmax]
        self.span_y = self.intensity[indmin:indmax]
        self.span_xmin = self.raman_shift[indmin]
        self.span_xmax = self.raman_shift[indmax]

        db_max_y = 0
        previous_db_max_y = 0
        db_sample_list = list(self.line_db_plot.keys())
        for sample in db_sample_list:
            db_max_y = max(previous_db_max_y, max(self.line_db_plot.get(sample).get_ydata()
                                                  [indmin:indmax]))
            previous_db_max_y = db_max_y

        if len(self.span_x) >= 2:
            self.line_main_plot.set_data(self.span_x, self.span_y)
            self.main_ax.set_xlim(self.span_x[0], self.span_x[-1])
            self.main_ax.set_ylim(
                self.span_y.min(), max(self.span_y.max(), db_max_y))
            self.main_fig.canvas.draw_idle()

    def getSpanSelection(self):
        return self.span_xmin, self.span_xmax, self.span_x, self.span_y

    def removeBaseline(self):
        baseObj = BaselineRemoval(self.intensity.flatten())
        self.intensity = baseObj.ZhangFit()
        norm = np.sqrt(sum(self.intensity**2))
        self.intensity = self.intensity / norm
        self.line_main_plot.set_data(self.raman_shift, self.intensity)
        self.main_ax.set_ylim(self.intensity.min(), self.intensity.max())
        self.line_span_plot.set_data(self.raman_shift, self.intensity)
        self.span_ax.set_ylim(self.intensity.min(), self.intensity.max())
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
            self.main_fig.savefig(save_filepath, dpi=400, transparent=False,
                                  facecolor=self.main_fig.get_facecolor(), edgecolor='none')

    def exportCameraImage(self):
        self.master.exportCameraImage()

    def clearPlot(self):
        self.clearDBPlot()
        self.main_ax.cla()
        self.span_ax.cla()
        self.main_ax.set_yticks([])
        self.span_ax.set_yticks([])
        self.span_ax.set_xticks([])
        self.span.clear()
        self.main_fig.canvas.draw_idle()

        self.configureButtons(
            ['save_file_button', 'export_image_button', 'remove_baseline_button'], 'disabled')
        self.master.configureButtons(
            'raman_search_frame', ['search_button'], 'disabled')

        self.master.initializeTreeview()

    def clearDBPlot(self):
        db_sample_list = list(self.line_db_plot.keys())

        for item in db_sample_list:
            self.line_db_plot[item].remove()
            self.line_db_plot.pop(item)

        self.main_ax.legend()
        self.main_fig.canvas.draw_idle()

    def changeSaveFolder(self, save_folder):
        self.save_folder = save_folder

    def plotSample(self, sample_name: str, raman_shift: np.ndarray, intensity: np.ndarray):
        norm = np.sqrt(sum(intensity**2))
        intensity = intensity / norm
        self.line_main_plot, = self.main_ax.plot(
            [], [], label=sample_name)
        self.line_main_plot.set_data(raman_shift, intensity)
        self.main_ax.set_xlim(
            raman_shift[0], raman_shift[-1])
        self.main_ax.set_ylim(
            intensity.min(), intensity.max())

        self.line_span_plot, = self.span_ax.plot([], [])
        self.line_span_plot.set_data(
            raman_shift, intensity)
        self.span_ax.set_xlim(
            raman_shift[0], raman_shift[-1])
        self.span_ax.set_ylim(
            intensity.min(), intensity.max())
        self.main_ax.set_yticks([])
        self.span_ax.set_yticks([])
        self.span_ax.set_xticks([])
        self.main_ax.legend()
        self.main_canvas.draw_idle()

        self.span_xmin = raman_shift[0]
        self.span_xmax = raman_shift[-1]

        self.remove_baseline_button.configure(state='normal')
        self.master.configureButtons(
            'raman_search_frame', ['search_button'], 'normal')
        self.configureButtons(['save_file_button', 'export_image_button',
                               'remove_baseline_button', 'clear_plot_button'], 'normal')

    def plotFromRamanDB(self, db_filepath, db_filename: str, add: bool):
        if add:
            self.line_db_plot[db_filename], = self.main_ax.plot(
                [], [], label=db_filename)
            db_raman_shift, db_intensity = np.loadtxt(
                db_filepath, unpack=True, delimiter=',')
            self.line_db_plot[db_filename].set_data(
                db_raman_shift, db_intensity)
        else:
            self.line_db_plot[db_filename].remove()
            self.line_db_plot.pop(db_filename)
        self.main_ax.legend()
        self.main_fig.canvas.draw_idle()

        # this updates max y on the plot
        self.OnSpanSelect(self.span_xmin, self.span_xmax)

    def configureButtons(self, buttons: tuple, state: str):
        button_dict = {'save_file_button': self.save_file_button, 'load_file_button': self.load_file_button, 'export_image_button': self.export_image_button,
                       'camera_button': self.camera_button, 'remove_baseline_button': self.remove_baseline_button, 'clear_plot_button': self.clear_plot_button}
        for button in buttons:
            button_dict.get(button).configure(state=state)
