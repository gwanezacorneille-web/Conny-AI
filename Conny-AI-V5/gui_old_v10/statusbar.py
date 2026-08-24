import customtkinter as ctk
import psutil
import datetime

from gui.theme import (
    SIDEBAR_COLOR,
    TEXT_COLOR,
    SMALL_FONT
)


class StatusBar(ctk.CTkFrame):

    def __init__(self, parent, **kwargs):

        super().__init__(
            parent,
            fg_color=SIDEBAR_COLOR,
            height=35,
            corner_radius=0,
            **kwargs
        )


        self.pack_propagate(False)


        self.label = ctk.CTkLabel(

            self,

            text="Starting Conny AI...",

            font=SMALL_FONT,

            text_color=TEXT_COLOR

        )


        self.label.pack(

            side="left",

            padx=15

        )


        self.update_status()



    def update_status(self):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        time = datetime.datetime.now().strftime(
            "%H:%M:%S"
        )


        status = (

            f"CPU: {cpu}%   |   "
            f"RAM: {ram}%   |   "
            f"Database: Connected   |   "
            f"Time: {time}"

        )


        self.label.configure(
            text=status
        )


        self.after(

            2000,

            self.update_status

        )
