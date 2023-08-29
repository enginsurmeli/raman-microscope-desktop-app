import customtkinter
import settings_window


class Menu(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        settings_button = customtkinter.CTkButton(
            self, text="Settings", command=self.OpenSettings)
        settings_button.pack(side="bottom", padx=10, pady=10)

    def OpenSettings(self):
        settings = settings_window.SettingsWindow(
            self.master, self.master.sendSettingsData())
