import customtkinter


class OnQuitApp(customtkinter.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        app_window_width = master.winfo_width()
        app_window_height = master.winfo_height()
        app_window_x = master.winfo_x()
        app_window_y = master.winfo_y()
        quit_window_width = 320
        quit_window_height = 100
        self.geometry(
            f"{quit_window_width}x{quit_window_height}+{app_window_x+app_window_width//2-quit_window_width//2}+{app_window_y+app_window_height//2-quit_window_height//2}")
        self.title("Quit Application")
        self.resizable(False, False)
        self.deiconify()
        self.grab_set()

        label = customtkinter.CTkLabel(
            self, text="Are you sure you want to quit?")
        label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        yes_button = customtkinter.CTkButton(
            self, text="Yes", command=self._quit)
        yes_button.grid(row=1, column=0, padx=10, pady=10)
        no_button = customtkinter.CTkButton(
            self, text="No", command=self.destroy)
        no_button.grid(row=1, column=1, padx=10, pady=10)

    def _quit(self):
        self.master.saveSettingsOnExit()
        self.master.disconnectDevices()
        self.master.quit()
        self.master.destroy()
