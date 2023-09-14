import customtkinter
from PIL import Image
import os
import settings_window


class CNCButtons(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        icons_folder = os.path.join(os.getcwd(), 'src', 'icons')

        inner_frame_padding = 5

        self.menu_buttons_frame = customtkinter.CTkFrame(self)
        self.menu_buttons_frame.pack(
            side="top",  expand=True, padx=inner_frame_padding, pady=inner_frame_padding)

        self.cnc_status_frame = customtkinter.CTkFrame(self)
        self.cnc_status_frame.pack(
            side="top",  expand=True, padx=inner_frame_padding, pady=inner_frame_padding)

        self.jog_buttons_frame = customtkinter.CTkFrame(self)
        self.jog_buttons_frame.pack(
            side="top",  expand=True, padx=inner_frame_padding, pady=inner_frame_padding)

        self.jog_settings_frame = customtkinter.CTkFrame(self)
        self.jog_settings_frame.pack(
            side="top",  expand=True, padx=inner_frame_padding, pady=inner_frame_padding)

        settings_button = customtkinter.CTkButton(
            self.menu_buttons_frame, text="Settings", command=self.openSettings)
        settings_button.pack()
        
        self.cnc_status_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.cnc_status_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        button_size = (30, 30)

        jog_button_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "jog_button_light.png")),
                                                  dark_image=Image.open(os.path.join(
                                                      icons_folder, "jog_button_dark.png")),
                                                  size=(13, 20))

        status_not_connected_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "status_not_connected_light.png")), dark_image=Image.open(os.path.join(
            icons_folder, "status_not_connected_dark.png")), size=button_size)

        status_alarm_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_folder, "status_alarm.png")))
        status_idle_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_folder, "status_idle.png")))
        status_jog_image = customtkinter.CTkImage(
            Image.open(os.path.join(icons_folder, "status_jog.png")))

        self.posx_label = customtkinter.CTkLabel(
            self.cnc_status_frame, text="X")
        self.posx_label.grid(
            row=0, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.posy_label = customtkinter.CTkLabel(
            self.cnc_status_frame, text="Y")
        self.posy_label.grid(
            row=0, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        self.posz_label = customtkinter.CTkLabel(
            self.cnc_status_frame, text="Z")
        self.posz_label.grid(
            row=0, column=2, padx=inner_frame_padding, pady=inner_frame_padding)

        self.posx_box = customtkinter.CTkEntry(self.cnc_status_frame, width=75)
        self.posx_box.grid(
            row=1, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.posy_box = customtkinter.CTkEntry(self.cnc_status_frame, width=75)
        self.posy_box.grid(
            row=1, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        self.posz_box = customtkinter.CTkEntry(self.cnc_status_frame, width=75)
        self.posz_box.grid(
            row=1, column=2, padx=inner_frame_padding, pady=inner_frame_padding)

        self.start_jog_button = customtkinter.CTkButton(
            self.cnc_status_frame, text="", command=self.startJog, width=button_size[0], height=button_size[1], image=jog_button_image)
        self.start_jog_button.grid(
            row=1, column=3, padx=inner_frame_padding, pady=inner_frame_padding)

        self.status_label = customtkinter.CTkLabel(
            self.cnc_status_frame, text="Status:")
        self.status_label.grid(
            row=2, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.status_box = customtkinter.CTkEntry(
            self.cnc_status_frame, state="disabled", width=100)
        self.status_box.grid(row=2, column=1, columnspan=2,
                             padx=inner_frame_padding, pady=inner_frame_padding, sticky="ew")

        self.status_led = customtkinter.CTkButton(
            self.cnc_status_frame, text="", state="disabled", width=button_size[0], height=button_size[1], corner_radius=100, fg_color="#dbdbdb")
        self.status_led.grid(
            row=2, column=3, padx=inner_frame_padding, pady=inner_frame_padding)

        yplus_icon_light = Image.open(os.path.join(
            icons_folder, "xy_axis_button_light.png"))
        yplus_icon_dark = Image.open(os.path.join(
            icons_folder, "xy_axis_button_dark.png"))
        yplus_icon = customtkinter.CTkImage(
            light_image=yplus_icon_light, dark_image=yplus_icon_dark, size=button_size)
        yminus_icon = customtkinter.CTkImage(light_image=yplus_icon_light.rotate(
            180), dark_image=yplus_icon_dark.rotate(180), size=button_size)
        xminus_icon = customtkinter.CTkImage(light_image=yplus_icon_light.rotate(
            90), dark_image=yplus_icon_dark.rotate(90), size=button_size)
        xplus_icon = customtkinter.CTkImage(light_image=yplus_icon_light.rotate(
            270), dark_image=yplus_icon_dark.rotate(270), size=button_size)
        zplus_icon_light = Image.open(os.path.join(
            icons_folder, "z_axis_button_light.png"))
        zplus_icon_dark = Image.open(os.path.join(
            icons_folder, "z_axis_button_dark.png"))
        zplus_icon = customtkinter.CTkImage(
            light_image=zplus_icon_light, dark_image=zplus_icon_dark, size=button_size)
        zminus_icon = customtkinter.CTkImage(light_image=zplus_icon_light.rotate(
            180), dark_image=zplus_icon_dark.rotate(180), size=button_size)
        cancel_jog_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(
            icons_folder, "cancel_button_light.png")), dark_image=Image.open(os.path.join(icons_folder, "cancel_button_dark.png")), size=button_size)

        self.jog_buttons_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.jog_buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.yplus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.move(axis='y+'), width=button_size[0], height=button_size[1], image=yplus_icon)
        self.yplus_button.grid(row=0, column=1, padx=inner_frame_padding,
                               pady=inner_frame_padding)

        self.yminus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.move(axis='y-'), width=button_size[0], height=button_size[1], image=yminus_icon)
        self.yminus_button.grid(
            row=2, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        self.xplus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.move(axis='x+'), width=button_size[0], height=button_size[1], image=xplus_icon)
        self.xplus_button.grid(row=1, column=2, padx=inner_frame_padding,
                               pady=inner_frame_padding)

        self.xminus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.move(axis='x-'), width=button_size[0], height=button_size[1], image=xminus_icon)
        self.xminus_button.grid(
            row=1, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.zplus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.move(axis='z+'), width=button_size[0], height=button_size[1], image=zplus_icon)
        self.zplus_button.grid(row=0, column=3, padx=inner_frame_padding,
                               pady=inner_frame_padding)

        self.zminus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.move(axis='z-'), width=button_size[0], height=button_size[1], image=zminus_icon)
        self.zminus_button.grid(
            row=2, column=3, padx=inner_frame_padding, pady=inner_frame_padding)

        self.cancel_jog_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=self.cancelJog, width=button_size[0], height=button_size[1], image=cancel_jog_icon)
        self.cancel_jog_button.grid(
            row=1, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        self.jog_settings_frame.rowconfigure((0, 1), weight=1)
        self.jog_settings_frame.columnconfigure(0, weight=1)
        self.jog_settings_frame.columnconfigure(1, weight=5)

        self.step_size_label = customtkinter.CTkLabel(
            self.jog_settings_frame, text="Step Size (mm)")
        self.step_size_label.grid(
            row=0, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.step_size_cbox = customtkinter.CTkComboBox(
            self.jog_settings_frame, values=['Continuous', "0.1", "0.5", "1", "5", "10", "50", "100"], justify="right")
        self.step_size_cbox.grid(
            row=0, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        self.feed_rate_label = customtkinter.CTkLabel(
            self.jog_settings_frame, text="Feed Rate (mm/min)")
        self.feed_rate_label.grid(
            row=1, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.feed_rate_cbox = customtkinter.CTkComboBox(
            self.jog_settings_frame, values=["10", "50", "100", "500", "1000", "2000"], justify="right")
        self.feed_rate_cbox.grid(
            row=1, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        # set default values for step size and feed rate
        self.step_size_cbox.set("1")
        self.feed_rate_cbox.set("2000")

    def openSettings(self):
        settings = settings_window.SettingsWindow(
            self.master, self.master.sendSettingsData())
    
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

    def startJog(self):
        pass

    def cancelJog(self):
        self.master.sendSerialCommand('cancel')
        # print(stop_command)

    def updateCNCConnectionStatus(self, status: str):
        if status == "not_connected":
            not_connected_status_color = "#dbdbdb" if customtkinter.get_appearance_mode() == "Light" else "#2b2b2b"
            self.start_jog_button.configure(fg_color=not_connected_status_color)
        elif status == "idle":
            self.start_jog_button.configure(fg_color='#fdbc40')
        elif status == "jog":
            self.start_jog_button.configure(fg_color='#33c748')
        elif status == "alarm":
            self.start_jog_button.configure(fg_color='#fc5753')
