import customtkinter as ctk

from gui.theme import (
    SIDEBAR_COLOR,
    TEXT_COLOR,
    TITLE_FONT,
    NORMAL_FONT,
    ACCENT_COLOR
)


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent, **kwargs):

        super().__init__(
            parent,
            fg_color=SIDEBAR_COLOR,
            width=220,
            corner_radius=0,
            **kwargs
        )


        self.pack_propagate(False)


        self.create_widgets()



    def create_widgets(self):


        # Logo / Title

        self.logo = ctk.CTkLabel(
            self,
            text="🤖\nCONNY AI\nV5.0",
            font=TITLE_FONT,
            text_color=TEXT_COLOR
        )

        self.logo.pack(
            pady=30
        )


        # Menu buttons

        buttons = [
            "💬 Chat",
            "🧠 Memory",
            "🌐 Internet",
            "🎤 Voice",
            "👁 Vision",
            "🧮 Tools",
            "🔌 Plugins",
            "⚙ Settings",
            "ℹ About"
        ]


        for item in buttons:

            button = ctk.CTkButton(

                self,

                text=item,

                height=40,

                font=NORMAL_FONT,

                fg_color="transparent",

                hover_color=ACCENT_COLOR,

                anchor="w"

            )


            button.pack(

                fill="x",

                padx=15,

                pady=5

            )
