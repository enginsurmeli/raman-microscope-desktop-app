import customtkinter
from PIL import Image
import os


class CNCButtons(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        icons_folder = os.path.join(os.getcwd(), 'src', 'icons')
        up_arrow_button_light = Image.open(os.path.join(
            icons_folder, "up_arrow_button_light.png"))
        up_arrow_button_dark = Image.open(os.path.join(
            icons_folder, "up_arrow_button_dark.png"))
        up_arrow_icon = customtkinter.CTkImage(
            light_image=up_arrow_button_light, dark_image=up_arrow_button_dark, size=(40, 40))
        down_arrow_icon = customtkinter.CTkImage(light_image=up_arrow_button_light.rotate(
            180), dark_image=up_arrow_button_dark.rotate(180), size=(40, 40))
        left_arrow_icon = customtkinter.CTkImage(light_image=up_arrow_button_light.rotate(
            90), dark_image=up_arrow_button_dark.rotate(90), size=(40, 40))
        right_arrow_icon = customtkinter.CTkImage(light_image=up_arrow_button_light.rotate(
            270), dark_image=up_arrow_button_dark.rotate(270), size=(40, 40))

        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.yplus_button = customtkinter.CTkButton(
            self, text="", command=lambda: self.move(axis='y+'), width=40, height=40, image=up_arrow_icon)
        self.yplus_button.grid(row=0, column=1, padx=10,
                               pady=10)

        self.yminus_button = customtkinter.CTkButton(
            self, text="", command=lambda: self.move(axis='y-'), width=40, height=40, image=down_arrow_icon)
        self.yminus_button.grid(
            row=2, column=1, padx=10, pady=10)

        self.xplus_button = customtkinter.CTkButton(
            self, text="", command=lambda: self.move(axis='x+'), width=40, height=40, image=right_arrow_icon)
        self.xplus_button.grid(row=1, column=2, padx=10,
                               pady=10)

        self.xminus_button = customtkinter.CTkButton(
            self, text="", command=lambda: self.move(axis='x-'), width=40, height=40, image=left_arrow_icon)
        self.xminus_button.grid(
            row=1, column=0, padx=10, pady=10)

        self.zplus_button = customtkinter.CTkButton(
            self, text="", command=lambda: self.move(axis='z+'), width=40, height=40, image=up_arrow_icon)
        self.zplus_button.grid(row=0, column=3, padx=10,
                               pady=10)

        self.zminus_button = customtkinter.CTkButton(
            self, text="", command=lambda: self.move(axis='z-'), width=40, height=40, image=down_arrow_icon)
        self.zminus_button.grid(
            row=2, column=3, padx=10, pady=10)

        self.stop_button = customtkinter.CTkButton(
            self, text="STOP", command=self.stop, width=40, height=40)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10)

        self.step_size_label = customtkinter.CTkLabel(
            self, text="Step Size (mm)")
        self.step_size_label.grid(
            row=3, column=0, padx=10, pady=10, sticky="ew")

        self.step_size_cbox = customtkinter.CTkComboBox(
            self, values=['Continuous', "0.1", "0.5", "1", "5", "10", "50", "100"], justify="right")
        self.step_size_cbox.grid(
            row=3, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

        self.feed_rate_label = customtkinter.CTkLabel(
            self, text="Feed Rate (mm/min)")
        self.feed_rate_label.grid(
            row=4, column=0, padx=10, pady=10, sticky="ew")

        self.feed_rate_cbox = customtkinter.CTkComboBox(
            self, values=["10", "50", "100", "500", "1000", "2000"], justify="right")
        self.feed_rate_cbox.grid(
            row=4, column=1, columnspan=3, padx=10, pady=10, sticky="ew")

        # set default values for step size and feed rate
        self.step_size_cbox.set("1")
        self.feed_rate_cbox.set("2000")

    def move(self, axis: str):
        if self.step_size_cbox.get() == "Continuous":
            step_size = 200
        else:
            try:
                step_size = float(self.step_size_cbox.get())
            except ValueError:
                return

        if '-' in axis:
            step_size = -step_size

        try:
            feed_rate = int(self.feed_rate_cbox.get())
        except ValueError:
            return

        x_step = 0
        y_step = 0
        z_step = 0

        if "x" in axis:
            x_step = step_size
        if "y" in axis:
            y_step = step_size
        if "z" in axis:
            z_step = step_size

        jog_command = f"$J=G21G91X{x_step:.3f}Y{y_step:.3f}Z{z_step:.3f}F{feed_rate}"
        self.master.sendSerialCommand(jog_command)
        # print(jog_command)

    def stop(self):
        self.master.sendSerialCommand('cancel')
        # print(stop_command)
