import tkinter as tk
from conny_brain import get_response
from conny_memory import remember, get_memory


class ConnyGUI:

    def __init__(self, root):

        self.root = root

        self.root.title("CONNY AI v1.3.1")
        self.root.geometry("700x600")
        self.root.resizable(False, False)


        # Header

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
            "CONNY AI v1.3.1\n"
            "System ready...\n\n"
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
            "Conny: " + response + "\n\n"
        )


        self.entry.delete(0, tk.END)



root = tk.Tk()

app = ConnyGUI(root)

root.mainloop()
