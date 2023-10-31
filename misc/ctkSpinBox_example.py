import customtkinter as ctk


class Spinbox(ctk.CTkFrame):
    def __init__(self, *args,
                 step_size: float = 1,
                 decimal_places: int = 0,
                 min_value, max_value,
                 **kwargs):
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(*args, **kwargs)

        self.step_size = step_size
        self.decimal_places = decimal_places

        self.grid_columnconfigure((0, 2), weight=0)
        self.grid_columnconfigure(1, weight=1)

        validation = self.register(self.only_numbers)

        self.entry = ctk.CTkEntry(
            self, width=50, border_width=0, validate="key", validatecommand=(validation, '%P'))
        self.entry.grid(row=0, column=1, columnspan=1,
                        padx=3, pady=3, sticky="nsew")

        entrybox_height = self.entry.winfo_reqheight() - 2

        self.subtract_button = ctk.CTkButton(self, text="-", width=entrybox_height, height=entrybox_height,
                                                        command=self.increment_callback('subtract'))
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.add_button = ctk.CTkButton(self, text="+", width=entrybox_height, height=entrybox_height,
                                        command=self.increment_callback('add'))
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, "0")
        # Bind all elements on mousewheel and keyboard events
        self.entry.bind("<MouseWheel>", self.on_mouse_wheel)
        self.subtract_button.bind("<MouseWheel>", self.on_mouse_wheel)
        self.add_button.bind("<MouseWheel>", self.on_mouse_wheel)
        self.bind("<MouseWheel>", self.on_mouse_wheel)

        self.entry.bind("<Up>", lambda e: self.increment_callback('add'))
        self.entry.bind(
            "<Down>", lambda e: self.increment_callback('subtract'))
        self.entry.bind("<FocusOut>", self.focusOutEvent)

    def increment_callback(self, operation: str = "add"):
        try:
            if operation == "add":
                value = float(self.entry.get()) + self.step_size
            if operation == "subtract":
                value = float(self.entry.get()) - self.step_size
            value = self.constrain(value, self.min_value, self.max_value)
            self.set(value)
        except ValueError:
            return

    def on_mouse_wheel(self, event):
        if event.delta > 0:
            self.increment_callback('add')
        else:
            self.increment_callback('subtract')

    def set(self, value: float):
        self.entry.delete(0, "end")
        str_value = f"{value:.{self.decimal_places}f}"
        self.entry.insert(0, str_value)

    def only_numbers(self, char):
        def is_float(char):
            try:
                float(char)
                return True
            except ValueError:
                return False

        # Validate true for only numbers
        if (is_float(char) or char == ""):
            return True
        else:
            return False

    def constrain(self, value, min_value, max_value):
        if value < min_value:
            return min_value
        elif value > max_value:
            return max_value
        else:
            return value

    def focusOutEvent(self, event):
        self.set(self.constrain(float(self.entry.get()),
                 self.min_value, self.max_value))


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Spinbox_sample")
        self.geometry(f"{400}x{100}")
        # Creating Main_Frame
        self.main_frame = ctk.CTkFrame(
            self, width=510, height=290, corner_radius=0)
        self.main_frame.grid(row=0, column=10, columnspan=10,
                             rowspan=10, ipadx=5, ipady=0, padx=0, pady=0, sticky="nw")
        self.main_frame.grid_rowconfigure(3, weight=1)
        # Spinboxes
        self.spinbox_hours = Spinbox(
            self.main_frame, step_size=0.1, min_value=0, max_value=10, decimal_places=1)
        self.spinbox_hours.grid(
            row=0, column=2, rowspan=1, ipadx=0, ipady=0, padx=0, pady=0)
        self.spinbox_hours.set(0)
        self.spinbox_minutes = Spinbox(
            self.main_frame, step_size=0.5, min_value=0, max_value=20, decimal_places=1)
        self.spinbox_minutes.grid(
            row=0, column=4, rowspan=1, ipadx=0, ipady=0, padx=0, pady=0)
        self.spinbox_minutes.set(0)
        self.spinbox_seconds = Spinbox(
            self.main_frame, step_size=1, min_value=0, max_value=100, decimal_places=0)
        self.spinbox_seconds.grid(
            row=0, column=6, rowspan=1, ipadx=0, ipady=0, padx=0, pady=0)
        self.spinbox_seconds.set(0)


if __name__ == "__main__":
    app = App()
    app.resizable(width=True, height=False)
    app.mainloop()
# https://github.com/TomSchimansky/CustomTkinter and CodeSame @2023
