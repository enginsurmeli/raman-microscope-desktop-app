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
        self.menu_buttons_frame.pack(side="top",  expand=True)

        self.cnc_status_frame = customtkinter.CTkFrame(self)
        self.cnc_status_frame.pack(side="top",  expand=True)

        self.jog_buttons_frame = customtkinter.CTkFrame(self)
        self.jog_buttons_frame.pack(side="top",  expand=True)

        self.jog_settings_frame = customtkinter.CTkFrame(self)
        self.jog_settings_frame.pack(side="top",  expand=True)

        # self.raman_scan_frame = customtkinter.CTkFrame(self)
        # self.raman_scan_frame.pack(
        #     side="top",  expand=True)

        button_size = (30, 30)

        self.menu_buttons_frame.grid_rowconfigure((0, 1), weight=1)
        self.menu_buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        home_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(
            icons_folder, "home_light.png")), dark_image=Image.open(os.path.join(icons_folder, "home_dark.png")), size=button_size)

        park_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(
            icons_folder, "park_light.png")), dark_image=Image.open(os.path.join(icons_folder, "park_dark.png")), size=button_size)

        center_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(
            icons_folder, "center_light.png")), dark_image=Image.open(os.path.join(icons_folder, "center_dark.png")), size=button_size)

        reset_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(
            icons_folder, "reset_light.png")), dark_image=Image.open(os.path.join(icons_folder, "reset_dark.png")), size=button_size)

        unlock_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(
            icons_folder, "unlock_light.png")), dark_image=Image.open(os.path.join(icons_folder, "unlock_dark.png")), size=button_size)

        settings_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(
            icons_folder, "settings_light.png")), dark_image=Image.open(os.path.join(icons_folder, "settings_dark.png")), size=button_size)

        home_button = customtkinter.CTkButton(self.menu_buttons_frame, text="Home", command=lambda: self.master.sendSerialCommand(
            '$H'), width=button_size[0], height=button_size[1], image=home_icon)
        home_button.grid(
            row=0, column=0, padx=inner_frame_padding, pady=inner_frame_padding, sticky="ew")

        park_button = customtkinter.CTkButton(self.menu_buttons_frame, text="Park", command=lambda: self.master.sendSerialCommand(
            'G0 X1 Y1 Z-1'), width=button_size[0], height=button_size[1], image=park_icon)
        park_button.grid(row=0, column=1, padx=inner_frame_padding,
                         pady=inner_frame_padding, sticky="ew")

        center_button = customtkinter.CTkButton(self.menu_buttons_frame, text="Center", command=lambda: self.master.sendSerialCommand(
            'G0 X145 Y80 Z-1'), width=button_size[0], height=button_size[1], image=center_icon)
        center_button.grid(
            row=0, column=2, padx=inner_frame_padding, pady=inner_frame_padding, sticky="ew")

        reset_button = customtkinter.CTkButton(self.menu_buttons_frame, text="Reset", command=lambda: self.master.sendSerialCommand(
            'reset'), width=button_size[0], height=button_size[1], image=reset_icon)
        reset_button.grid(
            row=1, column=0, padx=inner_frame_padding, pady=inner_frame_padding, sticky="ew")

        unlock_button = customtkinter.CTkButton(self.menu_buttons_frame, text="Unlock", command=lambda: self.master.sendSerialCommand(
            '$X'), width=button_size[0], height=button_size[1], image=unlock_icon)
        unlock_button.grid(
            row=1, column=1, padx=inner_frame_padding, pady=inner_frame_padding, sticky="ew")

        settings_button = customtkinter.CTkButton(
            self.menu_buttons_frame, text="Settings", command=self.openSettings, width=button_size[0], height=button_size[1], image=settings_icon)
        settings_button.grid(
            row=1, column=2, padx=inner_frame_padding, pady=inner_frame_padding)

        self.cnc_status_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.cnc_status_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        jog_button_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(icons_folder, "jog_button_light.png")),
                                                  dark_image=Image.open(os.path.join(
                                                      icons_folder, "jog_button_dark.png")),
                                                  size=button_size)

        entry_box_width = 75
        self.posx_box = customtkinter.CTkEntry(
            self.cnc_status_frame, width=entry_box_width, placeholder_text='X', justify="center")
        self.posx_box.grid(
            row=1, column=0, padx=inner_frame_padding, pady=inner_frame_padding, sticky="ns")

        self.posy_box = customtkinter.CTkEntry(
            self.cnc_status_frame, width=entry_box_width, placeholder_text='Y', justify="center")
        self.posy_box.grid(
            row=1, column=1, padx=inner_frame_padding, pady=inner_frame_padding, sticky="ns")

        self.posz_box = customtkinter.CTkEntry(
            self.cnc_status_frame, width=entry_box_width, placeholder_text='Z', justify="center")
        self.posz_box.grid(
            row=1, column=2, padx=inner_frame_padding, pady=inner_frame_padding, sticky="ns")

        self.start_run_button = customtkinter.CTkButton(
            self.cnc_status_frame, text="", command=self.startRun, width=button_size[0], height=button_size[1], image=jog_button_image)
        self.start_run_button.grid(
            row=1, column=3, padx=inner_frame_padding, pady=inner_frame_padding)

        status_label = customtkinter.CTkLabel(
            self.cnc_status_frame, text="Status:")
        status_label.grid(
            row=2, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.status_box = customtkinter.CTkEntry(
            self.cnc_status_frame, state="disabled", width=100, justify="center")
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
            self.jog_buttons_frame, text="", command=lambda: self.startJog(axis='y+'), width=button_size[0], height=button_size[1], image=yplus_icon)
        self.yplus_button.grid(row=0, column=1, padx=inner_frame_padding,
                               pady=inner_frame_padding)

        self.yminus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.startJog(axis='y-'), width=button_size[0], height=button_size[1], image=yminus_icon)
        self.yminus_button.grid(
            row=2, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        self.xplus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.startJog(axis='x+'), width=button_size[0], height=button_size[1], image=xplus_icon)
        self.xplus_button.grid(row=1, column=2, padx=inner_frame_padding,
                               pady=inner_frame_padding)

        self.xminus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.startJog(axis='x-'), width=button_size[0], height=button_size[1], image=xminus_icon)
        self.xminus_button.grid(
            row=1, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.zplus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.startJog(axis='z+'), width=button_size[0], height=button_size[1], image=zplus_icon)
        self.zplus_button.grid(row=0, column=3, padx=inner_frame_padding,
                               pady=inner_frame_padding)

        self.zminus_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=lambda: self.startJog(axis='z-'), width=button_size[0], height=button_size[1], image=zminus_icon)
        self.zminus_button.grid(
            row=2, column=3, padx=inner_frame_padding, pady=inner_frame_padding)

        # bind button release to stop continuous jog
        self.xplus_button.bind("<ButtonRelease-1>",
                               lambda event: self.stopContinuousJog())
        self.xminus_button.bind("<ButtonRelease-1>",
                                lambda event: self.stopContinuousJog())
        self.yplus_button.bind("<ButtonRelease-1>",
                               lambda event: self.stopContinuousJog())
        self.yminus_button.bind("<ButtonRelease-1>",
                                lambda event: self.stopContinuousJog())
        self.zplus_button.bind("<ButtonRelease-1>",
                               lambda event: self.stopContinuousJog())
        self.zminus_button.bind("<ButtonRelease-1>",
                                lambda event: self.stopContinuousJog())

        self.cancel_jog_button = customtkinter.CTkButton(
            self.jog_buttons_frame, text="", command=self.cancelJog, width=button_size[0], height=button_size[1], image=cancel_jog_icon)
        self.cancel_jog_button.grid(
            row=1, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        self.jog_settings_frame.rowconfigure((0, 1), weight=1)
        self.jog_settings_frame.columnconfigure(0, weight=1)
        self.jog_settings_frame.columnconfigure(1, weight=5)

        step_size_label = customtkinter.CTkLabel(
            self.jog_settings_frame, text="Step Size (mm)")
        step_size_label.grid(
            row=0, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.step_size_cbox = customtkinter.CTkComboBox(
            self.jog_settings_frame, width=entry_box_width*1.5, values=['Continuous', "0.1", "0.5", "1", "5", "10", "50", "100"], justify="right")
        self.step_size_cbox.grid(
            row=0, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        feed_rate_label = customtkinter.CTkLabel(
            self.jog_settings_frame, text="Feed Rate (mm/min)")
        feed_rate_label.grid(
            row=1, column=0, padx=inner_frame_padding, pady=inner_frame_padding)

        self.feed_rate_cbox = customtkinter.CTkComboBox(
            self.jog_settings_frame, width=entry_box_width*1.5, values=["10", "50", "100", "500", "1000", "2000"], justify="right")
        self.feed_rate_cbox.grid(
            row=1, column=1, padx=inner_frame_padding, pady=inner_frame_padding)

        # set default values for step size and feed rate
        self.step_size_cbox.set("1")
        self.feed_rate_cbox.set("2000")

        self.is_connected = False
        self.previous_state = None
        self.statusPolling()

        self.is_homed = False
        self.softlimit_x = 285
        self.softlimit_y = 150
        self.softlimit_z = -20

    def openSettings(self):
        settings = settings_window.SettingsWindow(
            self.master, self.master.sendSettingsData())

    def constrain(self, n, min_n, max_n):
        return max(min(n, max_n), min_n)

    def startJog(self, axis: str):
        if self.step_size_cbox.get() == "Continuous":
            step_size = 200
        else:
            step_size = float(self.step_size_cbox.get())

        if '-' in axis:
            step_size = -step_size

        feed_rate = int(self.feed_rate_cbox.get())

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

    def cancelJog(self):
        self.master.sendSerialCommand('cancel')

    def stopContinuousJog(self):
        if self.step_size_cbox.get() == "Continuous":
            self.cancelJog()

    def startRun(self):
        # constrain target position to soft limits
        target_x = self.constrain(
            float(self.posx_box.get()), 0, self.softlimit_x)
        target_y = self.constrain(
            float(self.posy_box.get()), 0, self.softlimit_y)
        target_z = self.constrain(
            float(self.posz_box.get()), self.softlimit_z, 0)

        self.master.sendSerialCommand(f"G0X{target_x}Y{target_y}Z{target_z}")

    def updateCNCStatus(self, status: str):
        state, *rest = status.split('|')
        state = state.replace('<', '')

        if rest and self.previous_state != 'Idle':
            posx, posy, posz = rest[0].split(',')
            posx = posx.replace('WPos:', '')
            # print(f"state: {state}, posx: {posx}, posy: {posy}, posz: {posz}")
            self.posx_box.delete(0, "end")
            self.posx_box.insert(0, f"{float(posx):.1f}")

            self.posy_box.delete(0, "end")
            self.posy_box.insert(0, f"{float(posy):.1f}")

            self.posz_box.delete(0, "end")
            self.posz_box.insert(0, f"{float(posz):.1f}")

        if state == "Connected":
            self.is_connected = True

        self.status_box.configure(state="normal")
        self.status_box.delete(0, "end")

        if state == "Disconnected":
            not_connected_status_color = "#2b2b2b" if customtkinter.get_appearance_mode(
            ) == "Light" else "#dbdbdb"
            self.status_led.configure(fg_color=not_connected_status_color)
            self.is_connected = False

        if state == "Idle":
            self.status_led.configure(fg_color='#fdbc40')
            self.is_homed = True
        if state == "Run" or state == "Jog":
            self.status_led.configure(fg_color='#33c748')

        if state == "Alarm":
            self.status_led.configure(fg_color='#fc5753')
            self.is_homed = False

        self.status_box.insert(0, state)
        self.status_box.configure(state="disabled")

        self.previous_state = state

    def statusPolling(self):
        if self.is_connected:
            self.master.sendSerialCommand('?')
        update_frequency = 4  # Hz
        self.after(round(1000//update_frequency),
                   self.statusPolling)
