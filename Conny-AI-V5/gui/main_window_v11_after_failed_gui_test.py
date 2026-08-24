import tkinter as tk
import threading
from datetime import datetime
from brain.brain import Brain


class ConnyNeuralSpace:
    def __init__(self, root):
        self.root = root

        # =====================================================
        # WINDOW
        # =====================================================

        self.root.title("CONNY AI • NEURAL SPACE")
        self.root.geometry("1280x760")
        self.root.minsize(950, 620)
        self.root.configure(bg="#050912")

        # =====================================================
        # COLORS
        # =====================================================

        self.bg = "#050912"
        self.panel = "#09121F"
        self.panel2 = "#0D1928"
        self.border = "#16314A"

        self.cyan = "#42E8FF"
        self.blue = "#248CFF"
        self.purple = "#8C6CFF"
        self.green = "#4DFF9A"

        self.white = "#EAF7FF"
        self.text = "#B8CBD9"
        self.dim = "#607586"

        # =====================================================
        # BRAIN
        # =====================================================

        self.brain = Brain()

        # =====================================================
        # BRAIN PROCESSING LOCK
        # =====================================================
        #
        # Brain.process() modifies shared state.
        # Only one Brain request may execute at a time.
        #

        self.brain_lock = threading.Lock()

        # =====================================================
        # LIVE STATUS LABELS
        # =====================================================

        self.status_labels = {}

        # =====================================================
        # BUILD GUI
        # =====================================================

        self.create_header()
        self.create_main_area()
        self.create_command_bar()

        # =====================================================
        # KEYBOARD SHORTCUTS
        # =====================================================

        self.root.bind("<Control-l>", self.clear_chat)
        self.root.bind("<Control-n>", self.new_chat)

        # =====================================================
        # STARTUP MESSAGE
        # =====================================================

        self.add_conny_message(
            "Neural connection established.\n"
            "All primary systems are online.\n\n"
            "Hello, Corneille. I'm ready."
        )

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.bg,
            height=82
        )

        header.pack(
            fill="x",
            padx=28,
            pady=(18, 5)
        )

        header.pack_propagate(False)

        # -----------------------------------------------------
        # CONNY CORE LOGO
        # -----------------------------------------------------

        logo = tk.Canvas(
            header,
            width=52,
            height=52,
            bg=self.bg,
            highlightthickness=0
        )

        logo.pack(side="left")

        logo.create_oval(
            8, 8, 44, 44,
            outline=self.cyan,
            width=2
        )

        logo.create_oval(
            17, 17, 35, 35,
            outline=self.blue,
            width=2
        )

        logo.create_oval(
            25, 25, 27, 27,
            fill=self.cyan,
            outline=""
        )

        # -----------------------------------------------------
        # TITLE
        # -----------------------------------------------------

        title = tk.Frame(
            header,
            bg=self.bg
        )

        title.pack(
            side="left",
            padx=12
        )

        tk.Label(
            title,
            text="CONNY",
            bg=self.bg,
            fg=self.white,
            font=("DejaVu Sans", 21, "bold")
        ).pack(anchor="w")

        tk.Label(
            title,
            text="NEURAL SPACE  //  V10",
            bg=self.bg,
            fg=self.cyan,
            font=("DejaVu Sans", 8, "bold")
        ).pack(anchor="w")

        # -----------------------------------------------------
        # LOCAL DATE / TIME
        # -----------------------------------------------------

        clock = tk.Frame(
            header,
            bg=self.bg
        )

        clock.pack(
            side="right",
            padx=(10, 12),
            pady=9
        )

        self.clock_time_label = tk.Label(
            clock,
            text="",
            bg=self.bg,
            fg=self.white,
            font=("DejaVu Sans", 9, "bold")
        )

        self.clock_time_label.pack(
            anchor="e"
        )

        self.clock_date_label = tk.Label(
            clock,
            text="",
            bg=self.bg,
            fg=self.dim,
            font=("DejaVu Sans", 7)
        )

        self.clock_date_label.pack(
            anchor="e"
        )

        self.update_local_clock()

        # -----------------------------------------------------
        # STATUS
        # -----------------------------------------------------

        status = tk.Frame(
            header,
            bg=self.bg
        )

        status.pack(
            side="right",
            pady=15
        )

        tk.Label(
            status,
            text="●",
            bg=self.bg,
            fg=self.green,
            font=("DejaVu Sans", 10)
        ).pack(side="left")

        tk.Label(
            status,
            text=" NEURAL SYSTEM ONLINE",
            bg=self.bg,
            fg=self.text,
            font=("DejaVu Sans", 9, "bold")
        ).pack(side="left")

        # -----------------------------------------------------
        # INFO BUTTON
        # -----------------------------------------------------

        info_button = tk.Button(
            header,
            text="CONNY AI  ⓘ",
            command=self.show_conny_info,
            bg=self.panel,
            fg=self.cyan,
            activebackground=self.panel2,
            activeforeground=self.white,
            relief="flat",
            bd=0,
            highlightbackground=self.border,
            highlightthickness=1,
            font=("DejaVu Sans", 8, "bold"),
            cursor="hand2",
            padx=14,
            pady=8
        )

        info_button.pack(
            side="right",
            padx=(10, 15)
        )

    # =========================================================
    # LOCAL DATE / TIME
    # =========================================================

    def update_local_clock(self):

        now = datetime.now()

        self.clock_time_label.configure(
            text=now.strftime("%H:%M:%S")
        )

        self.clock_date_label.configure(
            text=now.strftime("%A • %d %B %Y")
        )

        self.root.after(
            1000,
            self.update_local_clock
        )

    # =========================================================
    # MAIN AREA
    # =========================================================

    def create_main_area(self):

        main = tk.Frame(
            self.root,
            bg=self.bg
        )

        main.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=10
        )

        self.create_left_panel(main)
        self.create_chat_panel(main)
        self.create_right_panel(main)

        # Refresh live system status after all status widgets exist.
        self.refresh_system_status()

    # =========================================================
    # LEFT PANEL
    # =========================================================

    def create_left_panel(self, parent):

        panel = tk.Frame(
            parent,
            bg=self.panel,
            width=190,
            highlightbackground=self.border,
            highlightthickness=1
        )

        panel.pack(
            side="left",
            fill="y"
        )

        panel.pack_propagate(False)

        tk.Label(
            panel,
            text="NEURAL SYSTEM",
            bg=self.panel,
            fg=self.cyan,
            font=("DejaVu Sans", 9, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(20, 18)
        )

        systems = [
            ("MEMORY", "ACTIVE"),
            ("CONTEXT", "ACTIVE"),
            ("REASONING", "READY"),
            ("LEARNING", "READY"),
            ("KNOWLEDGE", "READY"),
            ("CODING", "READY"),
        ]

        for name, state in systems:

            row = tk.Frame(
                panel,
                bg=self.panel
            )

            row.pack(
                fill="x",
                padx=18,
                pady=7
            )

            tk.Label(
                row,
                text="◆",
                bg=self.panel,
                fg=self.cyan,
                font=("DejaVu Sans", 7)
            ).pack(side="left")

            tk.Label(
                row,
                text=name,
                bg=self.panel,
                fg=self.white,
                font=("DejaVu Sans", 8, "bold")
            ).pack(
                side="left",
                padx=7
            )

            tk.Label(
                row,
                text=state,
                bg=self.panel,
                fg=self.dim,
                font=("DejaVu Sans", 7)
            ).pack(
                side="right"
            )

    # =========================================================
    # CHAT PANEL
    # =========================================================

    def create_chat_panel(self, parent):

        panel = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        # -----------------------------------------------------
        # CHAT HEADER
        # -----------------------------------------------------

        top = tk.Frame(
            panel,
            bg=self.panel,
            height=48
        )

        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(
            top,
            text="◉  COMMAND CHANNEL",
            bg=self.panel,
            fg=self.white,
            font=("DejaVu Sans", 9, "bold")
        ).pack(
            side="left",
            padx=18,
            pady=14
        )

        tk.Label(
            top,
            text="SECURE",
            bg=self.panel,
            fg=self.cyan,
            font=("DejaVu Sans", 7, "bold")
        ).pack(
            side="right",
            padx=18
        )

        # -----------------------------------------------------
        # CHAT
        # -----------------------------------------------------

        self.chat = tk.Text(
            panel,
            bg=self.bg,
            fg=self.text,
            insertbackground=self.cyan,
            selectbackground="#17364D",
            relief="flat",
            bd=0,
            wrap="word",
            font=("DejaVu Sans", 10),
            padx=22,
            pady=18
        )

        self.chat.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1
        )

        self.chat.configure(
            state="disabled"
        )

        # -----------------------------------------------------
        # CHAT TAGS
        # -----------------------------------------------------

        self.chat.tag_configure(
            "conny",
            foreground=self.cyan,
            font=("DejaVu Sans", 9, "bold")
        )

        self.chat.tag_configure(
            "user",
            foreground=self.purple,
            font=("DejaVu Sans", 9, "bold")
        )

        self.chat.tag_configure(
            "message",
            foreground=self.text,
            font=("DejaVu Sans", 10)
        )

        # -----------------------------------------------------
        # PROCESSING INDICATOR
        # -----------------------------------------------------

        self.thinking_label = tk.Label(
            panel,
            text="",
            bg=self.panel,
            fg=self.cyan,
            font=("DejaVu Sans", 8, "bold")
        )

        self.thinking_label.pack(
            anchor="w",
            padx=18,
            pady=(4, 6)
        )

        self.thinking_visible = False

    # =========================================================
    # THINKING INDICATOR
    # =========================================================

    def show_thinking(self):

        if self.thinking_visible:
            return

        self.thinking_visible = True
        self.thinking_step = 0

        self._animate_thinking()

    def hide_thinking(self):

        self.thinking_visible = False

        self.thinking_label.configure(
            text=""
        )

    def _animate_thinking(self):

        if not self.thinking_visible:
            return

        dots = "." * (self.thinking_step % 4)

        self.thinking_label.configure(
            text="🧠 CONNY IS THINKING" + dots
        )

        self.thinking_step += 1

        self.root.after(
            450,
            self._animate_thinking
        )

    # =========================================================
    # RIGHT PANEL
    # =========================================================

    def create_right_panel(self, parent):

        panel = tk.Frame(
            parent,
            bg=self.panel,
            width=190,
            highlightbackground=self.border,
            highlightthickness=1
        )

        panel.pack(
            side="right",
            fill="y"
        )

        panel.pack_propagate(False)

        tk.Label(
            panel,
            text="SPACE STATUS",
            bg=self.panel,
            fg=self.cyan,
            font=("DejaVu Sans", 9, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(20, 18)
        )

        # -----------------------------------------------------
        # LIVE SYSTEM STATUS
        # -----------------------------------------------------

        self.status_labels = {}

        initial_status = self.get_system_status()

        for name, value in initial_status.items():

            self.status_item(
                panel,
                name,
                value
            )

        # -----------------------------------------------------
        # NEURAL CORE
        # -----------------------------------------------------

        tk.Label(
            panel,
            text="NEURAL CORE",
            bg=self.panel,
            fg=self.dim,
            font=("DejaVu Sans", 7, "bold")
        ).pack(
            pady=(45, 8)
        )

        core = tk.Canvas(
            panel,
            width=110,
            height=110,
            bg=self.panel,
            highlightthickness=0
        )

        core.pack()

        core.create_oval(
            10, 10, 100, 100,
            outline=self.border,
            width=2
        )

        core.create_oval(
            22, 22, 88, 88,
            outline=self.blue,
            width=2
        )

        core.create_oval(
            38, 38, 72, 72,
            outline=self.cyan,
            width=2
        )

        core.create_oval(
            53, 53, 57, 57,
            fill=self.cyan,
            outline=""
        )

    # =========================================================
    # LIVE SYSTEM STATUS
    # =========================================================

    def get_system_status(self):

        systems = {}

        # -----------------------------
        # NETWORK
        # -----------------------------

        try:
            systems["NETWORK"] = (
                "CONNECTED"
                if getattr(self.brain.online, "online", False)
                else "OFFLINE"
            )
        except Exception:
            systems["NETWORK"] = "UNKNOWN"

        # -----------------------------
        # BRAIN
        # -----------------------------

        systems["BRAIN"] = (
            "OPERATIONAL"
            if self.brain is not None
            else "OFFLINE"
        )

        # -----------------------------
        # MEMORY
        # -----------------------------

        systems["MEMORY"] = (
            "AVAILABLE"
            if self.brain.memory is not None
            else "OFFLINE"
        )

        # -----------------------------
        # KNOWLEDGE
        # -----------------------------

        systems["KNOWLEDGE"] = (
            "READY"
            if self.brain.knowledge is not None
            else "OFFLINE"
        )

        # -----------------------------
        # LEARNING
        # -----------------------------

        systems["LEARNING"] = (
            "READY"
            if self.brain.learning is not None
            else "OFFLINE"
        )

        # -----------------------------
        # SECURITY
        # -----------------------------

        systems["SECURITY"] = (
            "ACTIVE"
            if self.brain.security is not None
            else "OFFLINE"
        )

        return systems


    def refresh_system_status(self):

        status = self.get_system_status()

        for name, value in status.items():

            if name in self.status_labels:

                self.status_labels[name].configure(
                    text="●  " + value
                )


    # =========================================================
    # STATUS ITEM
    # =========================================================

    def status_item(self, parent, name, value):

        tk.Label(
            parent,
            text=name,
            bg=self.panel,
            fg=self.dim,
            font=("DejaVu Sans", 7, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(7, 0)
        )

        status_label = tk.Label(
            parent,
            text="●  " + value,
            bg=self.panel,
            fg=self.cyan,
            font=("DejaVu Sans", 8)
        )

        status_label.pack(
            anchor="w",
            padx=18
        )

        self.status_labels[name] = status_label

    # =========================================================
    # COMMAND BAR
    # =========================================================

    def create_command_bar(self):

        outer = tk.Frame(
            self.root,
            bg=self.bg,
            height=76
        )

        outer.pack(
            fill="x",
            padx=28,
            pady=(2, 18)
        )

        outer.pack_propagate(False)

        command = tk.Frame(
            outer,
            bg=self.panel2,
            highlightbackground=self.border,
            highlightthickness=1
        )

        command.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            command,
            text=">",
            bg=self.panel2,
            fg=self.cyan,
            font=("DejaVu Sans", 15, "bold")
        ).pack(
            side="left",
            padx=(18, 8)
        )

        self.entry = tk.Entry(
            command,
            bg=self.panel2,
            fg=self.white,
            insertbackground=self.cyan,
            relief="flat",
            bd=0,
            font=("DejaVu Sans", 10)
        )

        self.entry.pack(
            side="left",
            fill="both",
            expand=True,
            ipady=12
        )

        self.entry.insert(
            0,
            "Enter command..."
        )

        self.entry.bind(
            "<FocusIn>",
            self.clear_placeholder
        )

        self.entry.bind(
            "<Return>",
            self.send_message
        )

        tk.Button(
            command,
            text="EXECUTE  ➤",
            command=self.send_message,
            bg=self.cyan,
            fg="#041018",
            activebackground=self.blue,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("DejaVu Sans", 8, "bold"),
            cursor="hand2"
        ).pack(
            side="right",
            fill="y",
            padx=1,
            pady=1
        )

    # =========================================================
    # PLACEHOLDER
    # =========================================================

    def clear_placeholder(self, event=None):

        if self.entry.get() == "Enter command...":
            self.entry.delete(
                0,
                "end"
            )

    # =========================================================
    # CHAT CONTROLS
    # =========================================================

    def clear_chat(self, event=None):

        self.chat.configure(
            state="normal"
        )

        self.chat.delete(
            "1.0",
            "end"
        )

        self.chat.configure(
            state="disabled"
        )

        self.add_conny_message(
            "Conversation cleared.\n"
            "Neural channel remains active."
        )

        return "break"


    def new_chat(self, event=None):

        self.clear_chat()

        self.add_conny_message(
            "New conversation initialized.\n"
            "Hello, Corneille. I'm ready."
        )

        self.entry.focus_set()

        return "break"


    # =========================================================
    # CHAT FUNCTIONS
    # =========================================================

    def add_conny_message(self, message):

        self.chat.configure(
            state="normal"
        )

        self.chat.insert(
            "end",
            "\n◉ CONNY\n",
            "conny"
        )

        self.chat.insert(
            "end",
            message + "\n",
            "message"
        )

        self.chat.configure(
            state="disabled"
        )

        self.chat.see("end")

    def add_user_message(self, message):

        self.chat.configure(
            state="normal"
        )

        self.chat.insert(
            "end",
            "\n◆ YOU\n",
            "user"
        )

        self.chat.insert(
            "end",
            message + "\n",
            "message"
        )

        self.chat.configure(
            state="disabled"
        )

        self.chat.see("end")

    # =========================================================
    # BACKGROUND BRAIN WORKER
    # =========================================================

    def process_brain_worker(self, message, callback):
        """
        Run Brain.process() outside the Tkinter GUI thread.

        Tkinter widgets must NOT be accessed from this worker.
        The callback is scheduled by the caller on the GUI thread.
        """

        try:

            with self.brain_lock:

                answer = self.brain.process(
                    message
                )

            if answer is None:
                answer = "No response generated."

            callback(
                True,
                str(answer)
            )

        except Exception as error:

            callback(
                False,
                f"{type(error).__name__}: {error}"
            )

    # =========================================================
    # SEND MESSAGE
    # =========================================================

    def send_message(self, event=None):

        message = self.entry.get().strip()

        if not message:
            return "break"

        if message == "Enter command...":
            return "break"

        self.entry.delete(
            0,
            "end"
        )

        self.add_user_message(
            message
        )

        # -----------------------------------------------------
        # START BACKGROUND BRAIN PROCESSING
        # -----------------------------------------------------

        self.show_thinking()

        worker = threading.Thread(
            target=self.process_brain_worker,
            args=(
                message,
                self.brain_result_callback
            ),
            daemon=True
        )

        worker.start()

        return "break"

    def brain_result_callback(self, success, result):
        """
        Schedule the Brain result back onto the Tkinter GUI thread.
        """

        self.root.after(
            0,
            self._handle_brain_result,
            success,
            result
        )

    def _handle_brain_result(self, success, result):

        self.hide_thinking()

        if success:

            self.add_conny_message(
                str(result)
            )

        else:

            self.add_conny_message(
                "SYSTEM ERROR\n"
                f"{result}"
            )

    # =========================================================
    # CONNY AI INFORMATION WINDOW
    # =========================================================

    def show_conny_info(self):

        window = tk.Toplevel(
            self.root
        )

        window.title(
            "CONNY AI • SYSTEM INFORMATION"
        )

        window.geometry(
            "700x620"
        )

        window.minsize(
            620,
            500
        )

        window.configure(
            bg=self.bg
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        header = tk.Frame(
            window,
            bg=self.panel,
            height=105
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        # mini core
        core = tk.Canvas(
            header,
            width=65,
            height=65,
            bg=self.panel,
            highlightthickness=0
        )

        core.pack(
            side="left",
            padx=(25, 10),
            pady=18
        )

        core.create_oval(
            5, 5, 60, 60,
            outline=self.border,
            width=2
        )

        core.create_oval(
            15, 15, 50, 50,
            outline=self.blue,
            width=2
        )

        core.create_oval(
            27, 27, 38, 38,
            outline=self.cyan,
            width=2
        )

        core.create_oval(
            31, 31, 34, 34,
            fill=self.cyan,
            outline=""
        )

        title_frame = tk.Frame(
            header,
            bg=self.panel
        )

        title_frame.pack(
            side="left",
            pady=20
        )

        tk.Label(
            title_frame,
            text="CONNY AI",
            bg=self.panel,
            fg=self.white,
            font=("DejaVu Sans", 20, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            title_frame,
            text="NEURAL SPACE  //  SYSTEM INFORMATION",
            bg=self.panel,
            fg=self.cyan,
            font=("DejaVu Sans", 8, "bold")
        ).pack(
            anchor="w"
        )

        # -----------------------------------------------------
        # SCROLLABLE CONTENT
        # -----------------------------------------------------

        outer = tk.Frame(
            window,
            bg=self.bg
        )

        outer.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        canvas = tk.Canvas(
            outer,
            bg=self.bg,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            outer,
            orient="vertical",
            command=canvas.yview
        )

        content = tk.Frame(
            canvas,
            bg=self.bg
        )

        content.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=content,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # -----------------------------------------------------
        # CONNY INFORMATION
        # -----------------------------------------------------

        self.info_section(
            content,
            "🤖  CONNY AI",
            [
                ("Name", "CONNY AI"),
                ("Version", "V10"),
                ("Type", "AI Assistant"),
                ("Architecture", "Modular AI"),
                ("Mode", "Offline / Online"),
                ("Status", "OPERATIONAL"),
            ]
        )

        # -----------------------------------------------------
        # OWNER
        # -----------------------------------------------------

        self.info_section(
            content,
            "👤  OWNER / CREATOR",
            [
                ("Name", "Corneille"),
                ("Role", "Creator & Developer"),
                ("Project", "CONNY AI"),
            ]
        )

        # -----------------------------------------------------
        # CORE SYSTEMS
        # -----------------------------------------------------

        self.info_section(
            content,
            "🧠  CORE SYSTEMS",
            [
                ("Brain", "Operational"),
                ("Routing", "Operational"),
                ("Memory", "Operational"),
                ("Context", "Operational"),
                ("Knowledge", "Operational"),
                ("Reasoning", "Operational"),
                ("Coding", "Operational"),
                ("Emotion", "Operational"),
                ("Online Body", "Operational"),
            ]
        )

        # -----------------------------------------------------
        # V10 TEST STATUS
        # -----------------------------------------------------

        self.info_section(
            content,
            "🏆  V10 VALIDATION",
            [
                ("Master Gauntlet", "42 / 42 PASSED"),
                ("Routing Stress", "50 / 50 PASSED"),
                ("Regressions", "4 / 4 PASSED"),
                ("Final Fixture", "96 / 96 PASSED"),
                ("Success Rate", "100.0%"),
                ("V10 Status", "PASSED"),
            ]
        )

        # -----------------------------------------------------
        # PROJECT DESCRIPTION
        # -----------------------------------------------------

        self.info_section(
            content,
            "🌌  ABOUT THE PROJECT",
            [
                (
                    "Purpose",
                    "Personal AI assistant"
                ),
                (
                    "Interface",
                    "NEURAL SPACE"
                ),
                (
                    "Design",
                    "Futuristic command center"
                ),
                (
                    "Development",
                    "Modular architecture"
                ),
            ]
        )

        # -----------------------------------------------------
        # CLOSE BUTTON
        # -----------------------------------------------------

        tk.Button(
            window,
            text="CLOSE",
            command=window.destroy,
            bg=self.cyan,
            fg="#041018",
            activebackground=self.blue,
            activeforeground=self.white,
            relief="flat",
            bd=0,
            font=("DejaVu Sans", 8, "bold"),
            cursor="hand2",
            padx=30,
            pady=9
        ).pack(
            pady=(0, 20)
        )

    # =========================================================
    # INFORMATION SECTION
    # =========================================================

    def info_section(
        self,
        parent,
        title,
        items
    ):

        frame = tk.Frame(
            parent,
            bg=self.panel,
            highlightbackground=self.border,
            highlightthickness=1
        )

        frame.pack(
            fill="x",
            pady=7
        )

        tk.Label(
            frame,
            text=title,
            bg=self.panel,
            fg=self.cyan,
            font=("DejaVu Sans", 9, "bold")
        ).pack(
            anchor="w",
            padx=16,
            pady=(13, 8)
        )

        for name, value in items:

            row = tk.Frame(
                frame,
                bg=self.panel
            )

            row.pack(
                fill="x",
                padx=16,
                pady=3
            )

            tk.Label(
                row,
                text=name,
                bg=self.panel,
                fg=self.dim,
                width=20,
                anchor="w",
                font=("DejaVu Sans", 8)
            ).pack(
                side="left"
            )

            tk.Label(
                row,
                text=value,
                bg=self.panel,
                fg=self.white,
                anchor="w",
                font=("DejaVu Sans", 8, "bold")
            ).pack(
                side="left"
            )

        tk.Frame(
            frame,
            bg=self.panel,
            height=9
        ).pack()


# =============================================================
# LAUNCH
# =============================================================

def launch():

    root = tk.Tk()

    ConnyNeuralSpace(
        root
    )

    root.mainloop()


if __name__ == "__main__":
    launch()
