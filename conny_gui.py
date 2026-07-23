import tkinter as tk
from PIL import Image, ImageTk
from conny_brain import get_response
from conny_memory import remember, get_memory


class ConnyGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("CONNY AI v1.3.1")
        self.root.geometry("700x600")
        self.root.resizable(False, False)


        # Header

        self.logo = Image.open("assets/conny_logo.png")
        self.logo = self.logo.resize((80,80))

        self.logo_image = ImageTk.PhotoImage(self.logo)

        self.logo_label = tk.Label(
            root,
            image=self.logo_image
        )

        self.logo_label.pack()


 
        self.header = tk.Label(
            root,
            text="CONNY AI 🤖\nFrom a small idea to a global intelligence.\nCreated by Gwaneza Corneille Karenzi",
            font=("Arial", 14, "bold")
        )

        self.header.pack(pady=10)



        # Chat box

        self.chat = tk.Text(
            root,
            height=25,
            width=75,
            font=("Arial", 11)
        )

        self.chat.pack(padx=10)



        self.chat.insert(
            tk.END,
            "================================================\n"
            "🤖 CONNY AI v1.3.3\n\n"
            "From a small idea to a global intelligence.\n\n"
            "Created by:\n"
            "Gwaneza Corneille Karenzi\n\n"
            "Status: 🟢 Online\n"
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


        self.entry.bind("<Return>", lambda event: self.send())


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


        self.chat.insert(
            tk.END,
            "You: " + user + "\n"
        )


        if user.startswith("remember "):

            fact = user.replace("remember ", "", 1)

            remember(fact)

            response = "I will remember that."


        elif "what do you remember" in user:

            facts = get_memory()

            response = "\n".join(facts)


        else:

            response = get_response(user)


        self.chat.insert(
            tk.END,
            "Conny AI: " + response + "\n\n"
        )

        self.chat.see(tk.END)

        self.entry.delete(0, tk.END)



root = tk.Tk()

app = ConnyGUI(root)

root.mainloop()
