import customtkinter as ctk

from gui.theme import (
    CHAT_COLOR,
    TEXT_COLOR,
    NORMAL_FONT
)


class ChatWidget(ctk.CTkFrame):

    def __init__(self, parent, **kwargs):

        super().__init__(
            parent,
            fg_color=CHAT_COLOR,
            corner_radius=0,
            **kwargs
        )


        self.pack_propagate(False)


        self.create_chat_area()



    def create_chat_area(self):


        # Chat display

        self.chat_box = ctk.CTkTextbox(

            self,

            font=NORMAL_FONT,

            text_color=TEXT_COLOR,

            wrap="word",

            state="disabled"

        )


        self.chat_box.pack(

            fill="both",

            expand=True,

            padx=20,

            pady=20

        )



    def add_message(self, sender, message):


        self.chat_box.configure(

            state="normal"

        )


        self.chat_box.insert(

            "end",

            f"\n{sender}: {message}\n"

        )


        self.chat_box.configure(

            state="disabled"

        )


        self.chat_box.see("end")
