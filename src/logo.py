import os
import customtkinter
from PIL import Image

class Logo(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        # self.menu_logo_image = customtkinter.CTkImage(Image.open(
        #     os.path.join(master.image_path, "lst_logo.png")), size=(master.winfo_width(), 53*master.winfo_width()/131))
        # self.menu_logo = customtkinter.CTkLabel(
        #     self, image=self.menu_logo_image, text='')
        # self.menu_logo.pack(fill="both", expand=True)