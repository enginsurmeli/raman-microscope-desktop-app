import customtkinter
import tkinter as tk
from tkinter import ttk

import os
import numpy as np

from PIL import Image


class RamanSearch(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        self.initialdir = os.getcwd()
        self.raman_db_folder = 'raman_database'
        icons_folder = 'src\icons'
        button_size = (150, 35)
        icon_size = (button_size[1], button_size[1])
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # self.columns = ('match_percentage_column', 'sample_name_column')
        self.columns = ('sample_name_column', 'match_percentage_column')
        self.treeview = ttk.Treeview(
            self, columns=self.columns, show='headings')
        self.treeview.column(
            'match_percentage_column', width=100, anchor='center')
        self.treeview.column(
            'sample_name_column', width=200, anchor='center')
        self.treeview.heading('match_percentage_column', text="Correlation (%)", command=lambda: self.sortTreeviewColumn(
            self.treeview, 'match_percentage_column', True))
        self.treeview.heading('sample_name_column', text="Sample Name", command=lambda: self.sortTreeviewColumn(
            self.treeview, 'sample_name_column', False))
        self.treeview.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")

        search_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(self.initialdir, icons_folder, "search_light.png")),
                                             dark_image=Image.open(os.path.join(
                                                 self.initialdir, icons_folder, "search_dark.png")),
                                             size=icon_size)

        self.search_button = customtkinter.CTkButton(
            self, image=search_icon, text="Search", command=self.searchRamanDB)
        self.search_button.grid(row=1, column=0, padx=10, pady=(0, 10))

        scrollbar = customtkinter.CTkScrollbar(
            self, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

        self.treeview.bind("<Double-1>", self.onDoubleClick)

        self.initializeTreeview()
        self.configureButtons(['search_button'], 'disabled')

    def searchRamanDB(self):
        self.search_button.configure(text='Searching', state='disabled')
        self.initializeTreeview()
        self.master.clearDBPlot()
        self.master.configureButtons('raman_plot_frame', [
                                     'save_file_button', 'load_file_button', 'export_image_button', 'remove_baseline_button', 'clear_plot_button'], 'disabled')
        self.update_idletasks()

        span_xmin, span_xmax, raman_shift, intensity = self.master.getSpanSelection()

        # NOTE: To avoid redundancy, we assume that each database file has the same xmin and xmax.
        interp_size = 1024
        xmin = 150
        xmax = 1300

        search_xmin = max(xmin, span_xmin)
        search_xmax = min(xmax, span_xmax)
        xnew = np.linspace(xmin, xmax, interp_size)
        xnew_indices = np.where(np.logical_and(
            xnew >= search_xmin, xnew <= search_xmax))

        search_sample_intensity = np.interp(xnew, raman_shift, intensity, 0, 0)
        search_sample_intensity = search_sample_intensity[xnew_indices]

        for child in self.treeview.get_children():
            db_filename = self.treeview.item(child, 'values')[
                0]
            db_filepath = os.path.join(
                self.initialdir, self.raman_db_folder, f'{db_filename}.txt')
            with open(db_filepath, 'r') as f:
                _, db_intensity = np.loadtxt(
                    db_filepath, unpack=True, delimiter=',')
                search_db_intensity = db_intensity[xnew_indices]
                match_percentage = round(np.corrcoef(
                    search_sample_intensity, search_db_intensity)[0, 1] * 100)
                self.treeview.set(
                    child, column='match_percentage_column', value=match_percentage)

        self.search_button.configure(text='Search', state='normal')
        self.master.configureButtons('raman_plot_frame', [
                                     'save_file_button', 'load_file_button', 'export_image_button', 'remove_baseline_button', 'clear_plot_button'], 'normal')
        self.sortTreeviewColumn(self.treeview, 'match_percentage_column', True)

    def onDoubleClick(self, event):
        item = self.treeview.selection()[0]
        match_percentage = self.treeview.item(item, 'values')[-1]
        db_filename = self.treeview.item(item, 'values')[0]
        db_filepath = os.path.join(
            self.initialdir, self.raman_db_folder, db_filename + '.txt')  # TODO: change this to csv in the future

        if '<' not in db_filename:
            self.treeview.item(item, values=(
                '<' + db_filename, match_percentage))
            self.master.plotFromRamanDB(db_filepath, db_filename, add=True)
        else:
            db_filename = db_filename.replace('<', '')
            self.treeview.item(item, values=(
                db_filename, match_percentage))
            self.master.plotFromRamanDB(db_filepath, db_filename, add=False)

    def sortTreeviewColumn(self, treeview, column, reverse):
        l = [(treeview.set(k, column), k) for k in treeview.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)
            treeview.item(k, tags=('oddrow', 'evenrow')[index % 2])

        # reverse sort next time
        treeview.heading(column, command=lambda: self.sortTreeviewColumn(
            treeview, column, not reverse))

    def changeTheme(self, color_palette):
        small_font = ('None', 11)
        large_font = ('None', 12, 'bold')
        treestyle = ttk.Style()
        treestyle.theme_use('default')
        treestyle.configure("Treeview",
                            foreground=color_palette[3],
                            fieldbackground=color_palette[0],
                            borderwidth=0, font=small_font, rowheight=small_font[1]*3)
        self.treeview.tag_configure('oddrow', background=color_palette[0])
        self.treeview.tag_configure('evenrow', background=color_palette[4])
        treestyle.configure(
            "Treeview.Heading", background=color_palette[4], foreground=color_palette[3], borderwidth=0, relief='flat', font=large_font, rowheight=large_font[1]*4)
        treestyle.map('Treeview', background=[('selected', color_palette[1])],
                      foreground=[('selected', color_palette[2])])
        self.treeview.bind(
            "<<Treeview>>", lambda event: self.treeview.focus_set())  # remove focus from treeview

    def initializeTreeview(self):
        for item in self.treeview.get_children():
            self.treeview.delete(item)

        for subdir, dirs, files in os.walk(os.path.join(self.initialdir, self.raman_db_folder)):
            self.db_filepath_list = []
            for file in files:
                if file.endswith('.txt'):
                    # self.treeview.insert(
                    #     '', tk.END, values=('--', file.replace('.txt', '')))
                    self.treeview.insert(
                        '', tk.END, values=(file.replace('.txt', ''), '--'), tags=('oddrow', 'evenrow')[len(self.treeview.get_children()) % 2])
                    # TODO: Use this list inside SearchRamanDB method.
                    self.db_filepath_list.append(os.path.join(subdir, file))

    def configureButtons(self, buttons: tuple, state: str):
        button_dict = {'search_button': self.search_button}
        for button in buttons:
            button_dict.get(button).configure(state=state)
