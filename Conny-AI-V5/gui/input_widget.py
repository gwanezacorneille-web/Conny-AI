import customtkinter as ctk

from gui.theme import (
    CHAT_COLOR,
    TEXT_COLOR,
    NORMAL_FONT,
    ACCENT_COLOR
)


class InputWidget(ctk.CTkFrame):

    def __init__(self, parent, send_callback, **kwargs):

        super().__init__(
            parent,
            fg_color=CHAT_COLOR,
            corner_radius=0,
            **kwargs
        )

        self.send_callback = send_callback

        self.create_widgets()



    def create_widgets(self):

        self.entry = ctk.CTkEntry(
            self,
            placeholder_text="Type your message to Conny...",
            font=NORMAL_FONT,
            height=45,
            text_color=TEXT_COLOR
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(20,10),
            pady=10
        )


        self.entry.bind(
            "<Return>",
            self.send_message
        )


        self.send_button = ctk.CTkButton(

            self,

            text="➤ Send",

            height=45,

            width=100,

            font=NORMAL_FONT,

            fg_color=ACCENT_COLOR,

            command=self.send_message

        )


        self.send_button.pack(

            side="right",

            padx=(0,20),

            pady=10

        )



    def send_message(self, event=None):

        message = self.entry.get().strip()


        if message:

            self.entry.delete(
                0,
                "end"
            )

            self.send_callback(
                message
            )
