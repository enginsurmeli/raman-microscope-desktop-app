import customtkinter
import tkinter as tk
from tkinter import ttk

import os
import numpy as np

class RamanSearch(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        # Create Treeview for Raman Spectra match list
        self.treeview_frame = customtkinter.CTkFrame(master=self)
        self.treeview_frame.grid(
            row=0, column=2, padx=10, pady=20, sticky="nsew")
        self.treeview_frame.grid_rowconfigure(0, weight=5)
        self.treeview_frame.grid_rowconfigure(1, weight=1)
        self.treeview_frame.grid_columnconfigure(0, weight=15)
        self.treeview_frame.grid_columnconfigure(1, weight=1)
        
        # self.treeview_label = customtkinter.CTkLabel(
        #     master=self.treeview_frame, text="Raman Spectra Match List")
        # self.treeview_label.pack(side='top', pady=(10, 0))
        columns = ('match_percentage_column', 'sample_name_column')
        self.raman_db_treeview = ttk.Treeview(
            self.treeview_frame, columns=columns, show='headings')
        self.raman_db_treeview.column(
            'match_percentage_column', width=100, anchor='center')
        self.raman_db_treeview.column(
            'sample_name_column', width=200, anchor='center')
        self.raman_db_treeview.heading('match_percentage_column', text="Correlation (%)", command=lambda: self.SortTreeviewColumn(
            self.raman_db_treeview, 'match_percentage_column', True))
        self.raman_db_treeview.heading('sample_name_column', text="Sample Name", command=lambda: self.SortTreeviewColumn(
            self.raman_db_treeview, 'sample_name_column', False))
        self.raman_db_treeview.grid(
            row=0, column=0, padx=10, pady=10, sticky="nsew")
        # self.raman_db_treeview.pack(side='left', padx=(20, 0), pady=10, expand=False, anchor='nw')

        self.search_button = customtkinter.CTkButton(
            self.treeview_frame, text='Search', height=36, command=self.SearchRamanDB, state='disabled')
        self.search_button.grid(row=1, column=0, pady=(0, 10))

        # add a scrollbar
        scrollbar = customtkinter.CTkScrollbar(
            self.treeview_frame, command=self.raman_db_treeview.yview)
        self.raman_db_treeview.configure(yscrollcommand=scrollbar.set)
        # scrollbar.pack(side='right', fill='y')
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.raman_db_treeview.bind("<Double-1>", self.OnDoubleClick)
        
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
        
    def SearchRamanDB(self):
        # TODO: convert database files to .csv format.
        self.search_button.configure(text='Searching...', state='disabled')
        for child in self.raman_db_treeview.get_children():
            self.raman_db_treeview.set(child, column=0, value='--')
        self.update_idletasks()
        # NOTE: To avoid redundancy, we assume that each database file has the same xmin and xmax.
        # interp_size = 1024
        search_xmin = max(150.0, self.span_xmin)
        search_xmax = min(1300.0, self.span_xmax)
        # print(f"search_xmin: {search_xmin}, search_xmax: {search_xmax}")
        # search_sample_indices = np.where(np.logical_and(
        #     self.raman_shift >= search_xmin, self.raman_shift <= search_xmax))
        # search_sample_raman_shift = self.raman_shift[search_sample_indices]
        # xnew = np.linspace(search_xmin, search_xmax,  interp_size)
        # xnew = np.arange(search_xmin, search_xmax,
        #                  (1300.0 - 150.0)/interp_size)
        xnew = np.linspace(150, 1300, 1024)
        xnew_indices = np.where(np.logical_and(
            xnew >= search_xmin, xnew <= search_xmax))
        search_sample_intensity = np.interp(xnew, self.raman_shift, self.intensity, 0, 0)
        # search_sample_indices = np.where(np.logical_and(self.raman_shift >= search_xmin, self.raman_shift <= search_xmax))
        search_sample_intensity = search_sample_intensity[xnew_indices]
        for child in self.raman_db_treeview.get_children():
            db_filename = self.raman_db_treeview.item(
                child)["values"][-1].replace('<', '')
            db_filepath = os.path.join(
                self.initialdir, self.raman_db_folder, f'{db_filename}.txt')
            with open(db_filepath, 'r') as f:
                # header = [next(f) for x in range(4)]
                # name = header[0][8:].strip('\n')
                # id = header[1][10:].strip('\n')
                # chemistry = header[2][12:].strip('\n')
                db_raman_shift, db_intensity = np.loadtxt(
                    db_filepath, unpack=True, delimiter=',')
                # print(
                #     f"len(db_raman_shift): {len(db_raman_shift)}, len(db_intensity): {len(db_intensity)}")
                search_db_indices = np.where(np.logical_and(
                    db_raman_shift >= search_xmin, db_raman_shift <= search_xmax))
                search_db_raman_shift = db_raman_shift[xnew_indices]
                search_db_intensity = db_intensity[xnew_indices]
                # if db_filename == 'Abelsonite': # just for debugging once.
                #     print(f"sample name: {self.sample_name}")
                    # print(f"xnew_indices: {xnew_indices}, search_sample_indices: {search_sample_indices}, search_db_indices: {search_db_indices}")
                    # print(
                    #     f"len(search_sample_intensity): {len(search_sample_intensity)}, len(search_db_intensity): {len(search_db_intensity)}")
                    # print(
                    #     f"xnew: {xnew[xnew_indices]}, search_db_raman_shift: {search_db_raman_shift}")
                    # print(
                    #     f"xnew: {xnew[xnew_indices]}, search_sample_raman_shift: {search_sample_raman_shift}, search_db_raman_shift: {search_db_raman_shift}")
                    # print(
                    #     f"search_sample_raman_shift: {search_sample_raman_shift}, search_db_raman_shift: {search_db_raman_shift}, search_sample_intensity: {search_sample_intensity}, search_db_intensity: {search_db_intensity}")
                    # match_percentage = round(np.dot(
                    #     search_sample_intensity, search_db_intensity) * 100)
                    # print(f"xnew: {xnew[search_sample_indices]}, search_sample_intensity: {search_sample_intensity}")
                try:
                    match_percentage = round(np.corrcoef(
                        search_sample_intensity, search_db_intensity)[0, 1] * 100)
                except ValueError:
                    match_percentage = 0
                self.raman_db_treeview.set(
                    child, column=0, value=match_percentage)
        self.search_button.configure(text='Search', state='normal')
        self.SortTreeviewColumn(self.raman_db_treeview,
                                'match_percentage_column', True)

    def SortTreeviewColumn(self, treeview, col, reverse):
        l = [(treeview.set(k, col), k) for k in treeview.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            treeview.move(k, '', index)

        # reverse sort next time
        treeview.heading(col, command=lambda: self.SortTreeviewColumn(
            treeview, col, not reverse))
        
        