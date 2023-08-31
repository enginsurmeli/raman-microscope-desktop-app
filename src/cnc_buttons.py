import customtkinter


class CNCButtons(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.yplus_button = customtkinter.CTkButton(
            self, text="Y+", command=lambda: self.move(axis='y+'), width=10, height=10)
        self.yplus_button.grid(row=0, column=1, padx=10,
                               pady=10, sticky="nsew")

        self.yminus_button = customtkinter.CTkButton(
            self, text="Y-", command=lambda: self.move(axis='y-'))
        self.yminus_button.grid(
            row=2, column=1, padx=10, pady=10, sticky="nsew")

        self.xplus_button = customtkinter.CTkButton(
            self, text="X+", command=lambda: self.move(axis='x+'))
        self.xplus_button.grid(row=1, column=2, padx=10,
                               pady=10, sticky="nsew")

        self.xminus_button = customtkinter.CTkButton(
            self, text="X-", command=lambda: self.move(axis='x-'))
        self.xminus_button.grid(
            row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.zplus_button = customtkinter.CTkButton(
            self, text="Z+", command=lambda: self.move(axis='z+'))
        self.zplus_button.grid(row=0, column=3, padx=10,
                               pady=10, sticky="nsew")

        self.zminus_button = customtkinter.CTkButton(
            self, text="Z-", command=lambda: self.move(axis='z-'))
        self.zminus_button.grid(
            row=2, column=3, padx=10, pady=10, sticky="nsew")

        self.stop_button = customtkinter.CTkButton(
            self, text="STOP", command=self.stop)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

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
        self.feed_rate_cbox.set("100")

    def move(self, axis: str):
        if self.step_size_cbox.get() == "Continuous":
            step_size = "continuous"
        else:
            try:
                step_size = float(self.step_size_cbox.get())
                if '-' in axis:
                    step_size = -step_size
            except ValueError:
                return
        
        try: 
            feed_rate = int(self.feed_rate_cbox.get())
        except ValueError:
            return
        
        print(f"Moving {axis} axis by {step_size} mm at {feed_rate} mm/min")

    def stop(self):
        print("Stopping")
