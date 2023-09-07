import customtkinter
import tkinter as tk
from tkinter import ttk

import os
import numpy as np


class RamanSearch(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # self.label1 = customtkinter.CTkLabel(self, text="Raman Search")
        # self.label1.pack(fill="both", expand=True)

        self.master = master
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.columns = ('match_percentage_column', 'sample_name_column')
        self.treeview = ttk.Treeview(
            self, columns=self.columns, show='headings')
        self.treeview.column(
            'match_percentage_column', width=100, anchor='center')
        self.treeview.column(
            'sample_name_column', width=200, anchor='center')
        self.treeview.heading('match_percentage_column', text="Correlation (%)", command=lambda: self.SortTreeviewColumn(
            self.treeview, 'match_percentage_column', True))
        self.treeview.heading('sample_name_column', text="Sample Name", command=lambda: self.SortTreeviewColumn(
            self.treeview, 'sample_name_column', False))
        self.treeview.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.search_button = customtkinter.CTkButton(
            self, text="Search", command=self.ramanSearch, state="disabled")
        self.search_button.grid(row=1, column=0, padx=10, pady=(0, 10))

        scrollbar = customtkinter.CTkScrollbar(
            self, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.treeview.bind("<Double-1>", self.OnDoubleClick)

    def ramanSearch(self):
        pass

    def OnDoubleClick(self, event):
        pass

    def SortTreeviewColumn(self, treeview, column, reverse):
        l = [(treeview.set(k, column), k) for k in treeview.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        # reverse sort next time
        treeview.heading(column, command=lambda: self.SortTreeviewColumn(
            treeview, column, not reverse))
