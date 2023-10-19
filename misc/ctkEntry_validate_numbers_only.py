import customtkinter

# def only_numbers(char):
#     # Validate true for only numbers
#     if (is_float(char) or char==""):
#         return True
#     else:
#         return False

# def is_float(char):
#     try:
#         float(char)
#         return True
#     except ValueError:
#         return False

# root = customtkinter.CTk()

# validation = root.register(only_numbers)

# entry = customtkinter.CTkEntry(master=root, validate='key', validatecommand=(validation, '%P'))
# entry.pack(padx=10, pady=10)

# root.mainloop()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        validation = self.register(self.only_numbers)
        
        entry = customtkinter.CTkEntry(
            self, validate='key', validatecommand=(validation, '%P'))
        entry.pack(padx=10, pady=10)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()
