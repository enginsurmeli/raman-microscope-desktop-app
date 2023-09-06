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
        
        # Create Main Plot
        self.plot_frame = customtkinter.CTkFrame(master=self)
        self.plot_frame.grid(row=0, column=1,
                             padx=10, pady=20, sticky="nsew")

        # Plot something for placeholder inside the frames.
        # np.random.seed(19680801)
        px = 1/plt.rcParams['figure.dpi']  # pixel in inches
        self.fig, (self.main_plot, self.span_select_plot) = plt.subplots(2, figsize=(782*px, 850*px),
                                                                         gridspec_kw={'height_ratios': [7, 2]})

        self.line_main_plot, = self.main_plot.plot([], [])
        # self.line_span_select_plot, = self.span_select_plot.plot([], [])
        plt.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
        self.plotcanvas = FigureCanvasTkAgg(self.fig, self.plot_frame)
        # self.plotcanvas.get_tk_widget().pack(expand=True, fill="both")
        self.line_db_plot = {}

        self.toolbar = NavigationToolbar2Tk(
            self.plotcanvas, self.plot_frame, pack_toolbar=False)
        self.toolbar.config(background='#2b2b2b')
        self.toolbar.winfo_children()[-2].config(background='#2b2b2b')
        self.toolbar._message_label.config(
            background='#2b2b2b', foreground='#dce4ee')
        self.toolbar.update()
        self.toolbar.pack(side="bottom", fill='x', padx=(70, 20), expand=False)
        self.plotcanvas.get_tk_widget().pack(fill='both', expand=True)

        # Create Span Selector
        self.span = SpanSelector(self.span_select_plot, self.OnSpanSelect, "horizontal", useblit=True, props=dict(
            alpha=0.5, facecolor="tab:blue"), interactive=True, drag_from_anywhere=True, ignore_event_outside=False)

        # Create Mouseover Annotator
        self.OnMouseOver()
        
    def ThemeChanger(self, app_theme='Dark'):
        # print(self.theme_change_combo.get())
        # TODO: Implement light and system theme options. Keep selected theme as default.
        # Modes: "System" (standard), "Dark", "Light"
        customtkinter.set_appearance_mode(app_theme)
        color_palette = {'Light': ['#dbdbdb', '#dce4ee', '#1f6aa5', '#252526'], 'Dark': [
            '#2b2b2b', '#252526', '#1f6aa5', '#dce4ee']}
        # app_theme = app_theme
        app_theme = 'Dark'
        # Treeview theme color selection
        self.treestyle = ttk.Style()
        self.treestyle.theme_use('default')
        self.treestyle.configure("Treeview", background=color_palette[app_theme][0],
                                 foreground=color_palette[app_theme][3],
                                 fieldbackground=color_palette[app_theme][0],
                                 borderwidth=0)
        self.treestyle.configure(
            "Treeview.Heading", background=color_palette[app_theme][0], foreground=color_palette[app_theme][3], borderwidth=0)
        self.treestyle.map('Treeview', background=[('selected', color_palette[app_theme][1])],
                           foreground=[('selected', color_palette[app_theme][2])])
        self.raman_db_treeview.bind(
            "<<Treeview>>", lambda event: self.raman_db_treeview.focus_set())

        # Plot area theme color selection
        self.fig.set_facecolor(color_palette[app_theme][0])
        self.main_plot.set_facecolor(color_palette[app_theme][0])
        self.span_select_plot.set_facecolor(color_palette[app_theme][0])
        self.main_plot.tick_params(
            axis='x', colors=color_palette[app_theme][3])
        self.main_plot.xaxis.label.set_color(color_palette[app_theme][3])
        self.main_plot.spines['bottom'].set_color(color_palette[app_theme][3])
        self.main_plot.spines['top'].set_color(color_palette[app_theme][3])
        self.main_plot.spines['right'].set_color(color_palette[app_theme][3])
        self.main_plot.spines['left'].set_color(color_palette[app_theme][3])
        self.span_select_plot.spines['bottom'].set_color(
            color_palette[app_theme][3])
        self.span_select_plot.spines['top'].set_color(
            color_palette[app_theme][3])
        self.span_select_plot.spines['right'].set_color(
            color_palette[app_theme][3])
        self.span_select_plot.spines['left'].set_color(
            color_palette[app_theme][3])
        self.main_plot.set_yticks([])
        self.span_select_plot.set_yticks([])
        self.span_select_plot.set_xticks([])

    def OnDoubleClick(self, event):
        item = self.raman_db_treeview.selection()[0]
        match_percentage = self.raman_db_treeview.item(item, "values")[0]
        db_filename = self.raman_db_treeview.item(item, "values")[-1]
        db_filepath = os.path.join(
            self.initialdir, self.raman_db_folder, db_filename + '.txt')
        if '<' not in db_filename:
            self.raman_db_treeview.item(
                item, values=(match_percentage, '<' + db_filename))
            self.line_db_plot[db_filename], = self.main_plot.plot(
                [], [], label=db_filename)
            db_raman_shift, db_intensity = np.loadtxt(
                db_filepath, unpack=True, delimiter=',')
            self.line_db_plot[db_filename].set_data(
                db_raman_shift, db_intensity)
        else:
            db_filename = db_filename.replace('<', '')
            self.raman_db_treeview.item(
                item, values=(match_percentage, db_filename))
            self.line_db_plot[db_filename].remove()
            # self.line_db_plot[db_filename].set_data([], [])
        self.main_plot.legend()
        self.fig.canvas.draw_idle()

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
            self.fig.canvas.draw_idle()

    def OnMouseOver(self):
        annot = self.main_plot.annotate("", xy=(0, 0), xytext=(10, 10), textcoords="offset points",
                                        bbox=dict(boxstyle="round", fc="w"),
                                        arrowprops=dict(arrowstyle="->"))
        annot.set_visible(False)

        def update_annot(line, ind):
            posx, posy = [line.get_xdata()[ind], line.get_ydata()[ind]]
            annot.xy = (posx, posy)  # type: ignore
            text = f'{line.get_label()}: {posx:.2f}, {posy:.2f}'
            annot.set_text(text)
            annot.get_bbox_patch().set_alpha(1)  # type: ignore

        def hover(event):
            vis = annot.get_visible()
            if event.inaxes == self.main_plot:
                cont, index = self.line_main_plot.contains(
                    event)  # type: ignore
                if cont:
                    update_annot(self.line_main_plot, index["ind"][0])
                    annot.set_visible(True)
                if vis:
                    annot.set_visible(False)
                self.fig.canvas.draw_idle()

        # self.plotcanvas.draw()
        # self.plotcanvas.mpl_connect("motion_notify_event", hover)
        self.fig.canvas.mpl_connect("motion_notify_event", hover)

    def LoadSpectrumFile(self):
        filepath = fd.askopenfilename(
            initialdir=f"{self.initialdir}/{self.raman_db_folder}/", title="Select file", filetypes=(("all files", "*.*"), ("text files", "*.txt")))
        if filepath:  # if user wants to load specimen spectrum, open a file dialog
            self.search_button.configure(state='disabled')
            self.remove_baseline_button.configure(state='disabled')
            self.main_plot.cla()
            self.span_select_plot.cla()
            self.main_plot.set_yticks([])
            self.span_select_plot.set_yticks([])
            self.span_select_plot.set_xticks([])
            self.fig.canvas.draw_idle()
            for child in self.raman_db_treeview.get_children():
                # self.raman_db_treeview.set(child, column=0, value='--')
                self.raman_db_treeview.delete(child)

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
            self.line_span_select_plot, = self.span_select_plot.plot([], [])
            self.line_span_select_plot.set_data(
                self.raman_shift, self.intensity)
            self.span_select_plot.set_xlim(
                self.raman_shift[0], self.raman_shift[-1])
            self.span_select_plot.set_ylim(
                self.intensity.min(), self.intensity.max())
            self.main_plot.set_yticks([])
            self.span_select_plot.set_yticks([])
            self.span_select_plot.set_xticks([])
            self.main_plot.legend()
            self.fig.canvas.draw_idle()
            self.search_button.configure(state='normal')
            self.remove_baseline_button.configure(state='normal')

            self.span_xmin = self.raman_shift[0]
            self.span_xmax = self.raman_shift[-1]

            # Initialize Raman Spectra Database
            for subdir, dirs, files in os.walk(os.path.join(self.initialdir, self.raman_db_folder)):
                self.db_filepath_list = []
                for file in files:
                    if file.endswith('.txt'):
                        self.raman_db_treeview.insert(
                            '', tk.END, values=('--', file.replace('.txt', '')))
                        # TODO: Use this list inside SearchRamanDB method.
                        self.db_filepath_list.append(os.path.join(subdir, file))

    def RemoveBaseline(self):
        # TODO: apply spike removal to the specimen data.
        baseObj = BaselineRemoval(self.intensity.flatten())
        self.intensity = baseObj.ZhangFit()
        norm = np.sqrt(sum(self.intensity**2))  # type: ignore
        self.intensity = self.intensity / norm
        self.line_main_plot.set_data(self.raman_shift, self.intensity)
        self.main_plot.set_ylim(
            self.intensity.min(), self.intensity.max())
        self.line_span_select_plot.set_data(self.raman_shift, self.intensity)
        self.span_select_plot.set_ylim(
            self.intensity.min(), self.intensity.max())
        self.fig.canvas.draw_idle()
