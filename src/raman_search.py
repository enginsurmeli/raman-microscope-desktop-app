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
        button_size = (30, 30)
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
                                             size=button_size)

        self.search_button = customtkinter.CTkButton(
            self, image=search_icon, text="Search", command=self.ramanSearch, state="disabled")
        self.search_button.grid(row=1, column=0, padx=10, pady=(0, 10))

        scrollbar = customtkinter.CTkScrollbar(
            self, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)

        self.treeview.bind("<Double-1>", self.onDoubleClick)

        self.initializeTreeview()

    def ramanSearch(self):
        pass

    def onDoubleClick(self, event):
        item = self.treeview.selection()[0]
        match_percentage = self.treeview.item(item, 'values')[-1]
        db_filename = self.treeview.item(item, 'values')[0]
        db_filepath = os.path.join(
            self.initialdir, self.raman_db_folder, db_filename + '.txt')  # TODO: change this to csv in the future

        if '<' not in db_filename:
            self.treeview.item(item, values=(
                '<' + db_filename, match_percentage))
            self.master.plotFromLibrary(db_filepath, db_filename, add=True)
        else:
            db_filename = db_filename.replace('<', '')
            self.treeview.item(item, values=(
                db_filename, match_percentage))
            self.master.plotFromLibrary(db_filepath, db_filename, add=False)

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

    def configureButton(self, button: str, state: str):
        button_dict = {'search_button': self.search_button}
        button_dict.get(button).configure(state=state)
