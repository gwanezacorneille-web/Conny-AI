import customtkinter as ctk

from gui.theme import (
    APP_NAME,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    apply_theme
)

from gui.sidebar import Sidebar
from gui.chat_widget import ChatWidget
from gui.input_widget import InputWidget
from gui.statusbar import StatusBar

from brain.brain import Brain


class MainWindow(ctk.CTk):

    def __init__(self):

        apply_theme()

        super().__init__()


        self.title(APP_NAME)

        self.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )


        self.minsize(
            900,
            600
        )


        # Start Conny Brain

        self.brain = Brain()


        self.create_layout()



    def create_layout(self):


        self.grid_columnconfigure(
            1,
            weight=1
        )


        self.grid_rowconfigure(
            0,
            weight=1
        )


        # Sidebar

        self.sidebar = Sidebar(
            self
        )


        self.sidebar.grid(

            row=0,

            column=0,

            sticky="ns"

        )


        # Main area

        self.main_area = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )


        self.main_area.grid(

            row=0,

            column=1,

            sticky="nsew"

        )


        self.main_area.grid_columnconfigure(
            0,
            weight=1
        )


        self.main_area.grid_rowconfigure(
            0,
            weight=1
        )


        # Chat area

        self.chat = ChatWidget(
            self.main_area
        )


        self.chat.grid(

            row=0,

            column=0,

            sticky="nsew"

        )


        # Input area

        self.input = InputWidget(

            self.main_area,

            self.send_message

        )


        self.input.grid(

            row=1,

            column=0,

            sticky="ew"

        )


        # Status bar

        self.status = StatusBar(
            self
        )


        self.status.grid(

            row=1,

            column=0,

            columnspan=2,

            sticky="ew"

        )



    def send_message(self, message):


        # Display user message

        self.chat.add_message(
            "You",
            message
        )


        try:

            # Send message to Conny Brain

            reply = self.brain.process(
                message
            )


        except Exception as error:

            reply = (
                "Brain error: "
                + str(error)
            )


        # Display Conny response

        self.chat.add_message(
            "Conny",
            reply
        )



def start_gui():

    app = MainWindow()

    app.mainloop()



if __name__ == "__main__":

    start_gui()
