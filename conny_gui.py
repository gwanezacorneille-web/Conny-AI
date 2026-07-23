import tkinter as tk
from PIL import Image, ImageTk

from conny_brain import get_response
from conny_memory import remember, get_memory


class ConnyGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("CONNY AI v1.8")
        self.root.geometry("700x600")
        self.root.resizable(False, False)


        # Logo

        self.logo = Image.open("assets/conny_logo.png")
        self.logo = self.logo.resize((80, 80))

        self.logo_image = ImageTk.PhotoImage(self.logo)

        self.logo_label = tk.Label(
            root,
            image=self.logo_image
        )

        self.logo_label.pack()


        # Header

        self.header = tk.Label(
            root,
            text="CONNY AI 🤖\n"
                 "From a small idea to a global intelligence.\n"
                 "Created by Gwaneza Corneille Karenzi",
            font=("Arial", 14, "bold")
        )

        self.header.pack(pady=10)


        # Chat area

        self.chat = tk.Text(
            root,
            height=25,
            width=75,
            font=("Arial", 11),
            wrap=tk.WORD
        )

        self.chat.pack(padx=10)


        # Chat styles

        self.chat.tag_config(
            "user",
            font=("Arial", 11, "bold")
        )

        self.chat.tag_config(
            "conny",
            font=("Arial", 11, "bold")
        )


        # Welcome message

        self.chat.insert(
            tk.END,
            "================================================\n"
            "🤖 CONNY AI v1.8\n\n"
            "From a small idea to a global intelligence.\n\n"
            "Created by:\n"
            "Gwaneza Corneille Karenzi\n\n"
            "Status: 🟢 Online\n\n"
            "Features:\n"
            "🧠 Memory\n"
            "🧮 Calculator\n"
            "🌐 Online Knowledge\n"
            "💬 Smart Conversation\n"
            "================================================\n\n"
        )

        # Input area

        self.entry = tk.Entry(
            root,
            width=55,
            font=("Arial", 12)
        )

        self.entry.pack(
            side=tk.LEFT,
            padx=10,
            pady=10
        )


        # Enter key support

        self.entry.bind(
            "<Return>",
            lambda event: self.send()
        )


        # Send button

        self.button = tk.Button(
            root,
            text="Send",
            width=10,
            command=self.send
        )

        self.button.pack(
            side=tk.RIGHT,
            padx=10
        )


    def send(self):

        user = self.entry.get().lower().strip()


        if user == "":
            return


        # User message

        self.chat.insert(
            tk.END,
            "👤 You:\n",
            "user"
        )

        self.chat.insert(
            tk.END,
            user + "\n\n"
        )


        # Memory system

        if user.startswith("remember "):

            fact = user.replace(
                "remember ",
                "",
                1
            )

            remember(fact)

            response = "I will remember that."


        elif "what do you remember" in user:

            facts = get_memory()

            if facts:
                response = "\n".join(facts)
            else:
                response = "I don't remember anything yet."


        else:

            response = get_response(user)


        # Conny response

        self.chat.insert(
            tk.END,
            "🤖 Conny AI:\n",
            "conny"
        )

        self.chat.insert(
            tk.END,
            response + "\n\n"
        )


        self.chat.see(tk.END)

        self.entry.delete(
            0,
            tk.END
        )



root = tk.Tk()

app = ConnyGUI(root)

root.mainloop()
