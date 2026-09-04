from __future__ import annotations



import sys
from pathlib import Path

from .voice_engine import ConnyVoiceEngine
from .voice_bridge import ConnyVoiceBridge
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from .emoji_engine import emoji_context

from .theme_manager import ThemeManager

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPainter
from PyQt6.QtWidgets import (
    QRadioButton,
    QGroupBox,
    QDialogButtonBox,
    QDialog,
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

# Automatic TTS for normal chat answers is OFF. Voice remains available.
AUTO_SPEAK_RESPONSES = False

V13_ROOT = Path(__file__).resolve().parents[1]

if str(V13_ROOT) not in sys.path:
    sys.path.insert(0, str(V13_ROOT))

from bridge import get_bridge
from shared.models import ConnyRequest


class BrainWorker(QThread):
    finished = pyqtSignal(str)
    failed = pyqtSignal(str)

    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def run(self):
        try:
            bridge = get_bridge()
            response = bridge.handle(
                ConnyRequest(message=self.message)
            )

            if not response.success:
                self.failed.emit(
                    getattr(response, "text", None)
                    or "CONNY could not process the request."
                )
                return

            self.finished.emit(response.text or "")
        except Exception as exc:
            self.failed.emit(f"Error: {exc}")



class MessageBubble(QFrame):
    def __init__(self, text: str, sender: str):
        super().__init__()

        self.sender = sender

        self.setObjectName(
            "userBubble" if sender == "user" else "connyBubble"
        )

        # ----------------------------------------------------
        # REAL VISIBLE CHAT BUBBLE
        # ----------------------------------------------------
        if sender == "conny":
            self.setStyleSheet("""
                QFrame#connyBubble {
                    background-color: #181818;
                    border: 2px solid #444444;
                    border-radius: 18px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame#userBubble {
                    background-color: #242424;
                    border: 1px solid #444444;
                    border-radius: 18px;
                }
            """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(
            16, 12, 16, 12
        )
        layout.setSpacing(5)

        sender_row = QHBoxLayout()
        sender_row.setSpacing(7)

        identity = QLabel(
            "YOU" if sender == "user" else "◈ CONNY AI"
        )
        identity.setObjectName("bubbleSender")

        sender_row.addWidget(identity)
        sender_row.addStretch()

        layout.addLayout(sender_row)

        message = QLabel(text)
        message.setObjectName("bubbleText")
        message.setWordWrap(True)
        message.setMinimumHeight(0)
        message.setMaximumHeight(16777215)
        message.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        message.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        layout.addWidget(message)

        # Keep the answer readable and give the bubble
        # enough width to visibly surround the text.
        self.setMinimumWidth(220)
        self.setMaximumWidth(740)

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Minimum
        )


class ConnyWatermark(QLabel):
    """Subtle non-interactive CONNY AI center watermark."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("connyWatermark")
        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents,
            True
        )
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText(
            "CONNY AI\n"
            "UNDERSTAND  •  REASON  •  ACT  •  VERIFY  •  IMPROVE"
        )

        font = QFont()
        font.setBold(True)
        font.setPointSize(16)
        self.setFont(font)

        self.setStyleSheet("""
            QLabel#connyWatermark {
                background: transparent;
                color: rgba(255, 255, 255, 12);
                border: none;
                padding: 0px;
            }
        """)

        self.lower()

    def resizeEvent(self, event):
        super().resizeEvent(event)

        parent = self.parentWidget()
        if parent is not None:
            self.setGeometry(parent.rect())


class ConnyDesktopWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # ====================================================
        # CONNY VOICE
        # ====================================================

        self._voice_engine = ConnyVoiceEngine()
        self._voice_bridge = ConnyVoiceBridge()
        self._voice_busy = False

        self.worker = None
        self._last_emoji_context = ""
        self.sidebar_buttons = []

        self.setWindowTitle("CONNY AI V13")
        self.resize(1200, 760)
        self.setMinimumSize(900, 600)

        self.build_ui()

        self.theme_manager = ThemeManager(
            QApplication.instance()
        )

    # ========================================================
    # MAIN UI
    # ========================================================

    def build_ui(self):

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ====================================================
        # SIDEBAR
        # ====================================================

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(215)
        sidebar.setMaximumWidth(245)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(14, 14, 14, 14)
        sidebar_layout.setSpacing(5)

        # Brand
        brand_row = QHBoxLayout()
        brand_row.setSpacing(10)

        compass = QLabel("◈")
        compass.setObjectName("sidebarCompass")

        brand = QLabel("CONNY AI")
        brand.setObjectName("sidebarBrand")

        brand_row.addWidget(compass)
        brand_row.addWidget(brand)
        brand_row.addStretch()

        sidebar_layout.addLayout(brand_row)

        creator = QLabel("Gwaneza Corneille Karenzi")
        creator.setObjectName("sidebarCreator")
        sidebar_layout.addWidget(creator)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setObjectName("sidebarLine")
        sidebar_layout.addWidget(line)

        sidebar_layout.addSpacing(10)

        # Navigation
        self._add_sidebar_button(
            sidebar_layout, "⌂", "Chat", True
        )

        self._add_sidebar_button(
            sidebar_layout, "◉", "Brain"
        )

        self._add_sidebar_button(
            sidebar_layout, "◌", "Voice"
        )

        self._add_sidebar_button(
            sidebar_layout, "◇", "Memory"
        )

        self._add_sidebar_button(
            sidebar_layout, "⌘", "Plugins"
        )

        self._add_sidebar_button(
            sidebar_layout, "⚒", "Tools"
        )

        sidebar_layout.addStretch()

        self.settings_button = self._add_sidebar_button(
            sidebar_layout, "⚙", "Settings"
        )
        self.settings_button.clicked.connect(
            self.show_settings
        )

        self._add_sidebar_button(
            sidebar_layout, "ⓘ", "About"
        )

        sidebar_status = QLabel(
            "●  SYSTEM ONLINE"
        )
        sidebar_status.setObjectName("sidebarStatus")
        sidebar_layout.addWidget(sidebar_status)

        root_layout.addWidget(sidebar)

        # ====================================================
        # MAIN PANEL
        # ====================================================

        main_panel = QFrame()
        main_panel.setObjectName("mainPanel")

        main_layout = QVBoxLayout(main_panel)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ====================================================
        # TOP HEADER
        # ====================================================

        header = QFrame()
        header.setObjectName("header")
        header.setMinimumHeight(78)

        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(18, 10, 18, 8)
        header_layout.setSpacing(2)

        title = QLabel("♛  CONNY AI V13")
        title.setObjectName("mainTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel(
            "Understand  •  Reason  •  Act  •  Verify  •  Improve"
        )
        subtitle.setObjectName("mainSubtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)

        main_layout.addWidget(header)

        # ====================================================
        # CHAT
        # ====================================================

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scroll.setObjectName("chatScroll")

        self.chat_container = QWidget()

        self.conny_watermark = ConnyWatermark(self.chat_container)
        self.conny_watermark.setGeometry(
            self.chat_container.rect()
        )
        self.conny_watermark.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.conny_watermark.lower()
        self.chat_container.setObjectName("chatContainer")

        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setContentsMargins(
            24, 18, 24, 18
        )
        self.chat_layout.setSpacing(12)

        self.chat_layout.addStretch()

        self.scroll.setWidget(self.chat_container)

        main_layout.addWidget(self.scroll, 1)

        # ====================================================
        # THINKING
        # ====================================================

        self.thinking = QLabel(
            "●  CONNY READY"
        )
        self.thinking.setObjectName("thinking")
        self.thinking.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(self.thinking)

        # ====================================================
        # COMPOSER
        # ====================================================

        composer_outer = QFrame()
        composer_outer.setObjectName("composerOuter")

        composer_layout = QHBoxLayout(composer_outer)
        composer_layout.setContentsMargins(
            16, 8, 16, 8
        )
        composer_layout.setSpacing(6)

        self.attach_button = QPushButton("＋")
        self.attach_button.setObjectName("composerIcon")
        self.attach_button.setToolTip(
            "Attachments"
        )

        self.emoji_button = QPushButton("☺")
        self.emoji_button.clicked.connect(self.show_emoji_picker)
        self.emoji_button.setObjectName("composerIcon")
        self.emoji_button.setToolTip(
            "Emoji"
        )

        self.input = QLineEdit()
        self.input.setObjectName("messageInput")
        self.input.setPlaceholderText(
            "Message CONNY AI..."
        )
        self.input.returnPressed.connect(
            self.send_message
        )

        self.voice_button = QPushButton("🎙")

        # V13 manual response playback button.
        self._conny_manual_speak_button = QPushButton("🔊")
        self._conny_manual_speak_button.setObjectName("composerIcon")
        self._conny_manual_speak_button.setToolTip(
            "Read the latest CONNY AI response aloud"
        )
        self._conny_manual_speak_button.clicked.connect(
            self._conny_speak_latest_response
        )

        self.voice_button.setObjectName("composerIcon")
        self.voice_button.setMinimumSize(52, 52)
        self.voice_button.setMaximumSize(72, 72)
        self.voice_button.setToolTip("Voice input — click to speak")
        # V13 voice-button usability fix:
        # enlarge the actual clickable hit area without changing the GUI layout.
        self.voice_button.setMinimumWidth(60)
        self.voice_button.setMinimumHeight(52)
        self.voice_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.voice_button.setToolTip("Click to speak")

        self.voice_button.setToolTip(
            "Voice"
        )
        self.voice_button.clicked.connect(
            self.conny_voice_listen
        )

        self.new_button = QPushButton("NEW")
        self.new_button.setObjectName(
            "secondaryButton"
        )
        self.new_button.clicked.connect(
            self.new_chat
        )

        self.send_button = QPushButton("↑")
        self.send_button.setObjectName(
            "sendButton"
        )
        self.send_button.setToolTip(
            "Send message"
        )
        self.send_button.clicked.connect(
            self.send_message
        )

        composer_layout.addWidget(
            self.attach_button
        )
        composer_layout.addWidget(
            self.emoji_button
        )
        composer_layout.addWidget(
            self.input, 1
        )
        composer_layout.addWidget(
            self.voice_button
        )
        composer_layout.addWidget(
            self.new_button
        )
        composer_layout.addWidget(
            self.send_button
        )

        main_layout.addWidget(composer_outer)

        # ====================================================
        # STATUS BAR
        # ====================================================

        footer = QFrame()
        footer.setObjectName("footer")

        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(
            16, 5, 16, 5
        )

        brain_status = QLabel(
            "●  Brain Online"
        )
        brain_status.setObjectName(
            "footerStatusOnline"
        )

        voice_status = QLabel(
            "●  Voice Ready"
        )
        voice_status.setObjectName(
            "footerStatusOnline"
        )

        version_status = QLabel(
            "CONNY AI V13  •  DESKTOP"
        )
        version_status.setObjectName(
            "footerVersion"
        )

        footer_layout.addWidget(
            brain_status
        )
        footer_layout.addSpacing(18)
        footer_layout.addWidget(
            voice_status
        )
        footer_layout.addStretch()
        footer_layout.addWidget(
            version_status
        )

        main_layout.addWidget(footer)

        root_layout.addWidget(
            main_panel, 1
        )

        # Initial message
        self.add_conny_message(
            "Hello! 👋 I'm CONNY AI V13. "
            "How can I help you?"
        )

    # ========================================================
    # SIDEBAR
    # ========================================================

    def _add_sidebar_button(
        self,
        layout,
        icon,
        text,
        active=False
    ):
        button = QPushButton(
            f"  {icon}   {text}"
        )
        button.setObjectName(
            "sidebarButtonActive"
            if active
            else "sidebarButton"
        )
        button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        layout.addWidget(button)
        self.sidebar_buttons.append(button)

        return button

    # ========================================================
    # CHAT
    # ========================================================

    def add_user_message(self, text: str):
        bubble = MessageBubble(
            text,
            "user"
        )

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            bubble,
            alignment=Qt.AlignmentFlag.AlignRight
        )

        self.scroll_to_bottom()

    def add_conny_message(self, text: str):
        bubble = MessageBubble(
            text,
            "conny"
        )

        self.chat_layout.insertWidget(
            self.chat_layout.count() - 1,
            bubble,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

        self.scroll_to_bottom()

    def scroll_to_bottom(self):
        QApplication.processEvents()

        bar = self.scroll.verticalScrollBar()

        bar.setValue(
            bar.maximum()
        )

    # ========================================================
    # SEND
    # ========================================================


    # ========================================================
    # STAGE 9.9 — EMOJI PICKER
    # ========================================================

    def show_emoji_picker(self):
        """Show the CONNY emoji picker from the existing button."""

        menu = QMenu(self)
        menu.setObjectName("emojiMenu")

        emojis = [
            "😀", "😃", "😄", "😁", "😆", "😂", "🤣", "😊",
            "😍", "🥰", "😘", "😎", "🤔", "🤨", "😐", "🙄",
            "😢", "😭", "😡", "😱", "😳", "🥺", "😴", "🤩",
            "🥳", "🤯", "👍", "👎", "👏", "🙌", "🙏", "🤝",
            "✌️", "👌", "💪", "❤️", "🧡", "💛", "💚", "💙",
            "💜", "🖤", "🤍", "💔", "💕", "💖", "💯", "🔥",
            "⭐", "🌟", "✨", "⚡", "🎉", "🎊", "🚀", "💡",
            "🧠", "👑", "🤖", "💻", "📱", "🎮", "⚽", "🏀",
            "🎵", "🎶", "📚", "🔧", "🛠️", "✅", "❌", "⚠️",
            "❓", "❗", "💬", "🌍", "🌈", "☀️", "🌙",
        ]

        for emoji in emojis:
            action = menu.addAction(emoji)
            action.setData(emoji)
            action.triggered.connect(
                lambda checked=False, e=emoji: self.insert_emoji(e)
            )

        menu.setStyleSheet("""
            QMenu#emojiMenu {
                background: #111827;
                color: #ffffff;
                border: 1px solid #344054;
                padding: 8px;
            }

            QMenu#emojiMenu::item {
                padding: 8px 10px;
                font-size: 20px;
                border-radius: 6px;
            }

            QMenu#emojiMenu::item:selected {
                background: #263244;
            }
        """)

        if hasattr(self, "emoji_button"):
            menu.exec(
                self.emoji_button.mapToGlobal(
                    self.emoji_button.rect().bottomLeft()
                )
            )
        else:
            menu.exec(
                self.input.mapToGlobal(
                    self.input.rect().bottomLeft()
                )
            )

    def insert_emoji(self, emoji: str):
        """Insert a selected emoji into the existing message field."""
        if not emoji:
            return

        cursor = self.input.cursorPosition()
        current = self.input.text()

        self.input.setText(
            current[:cursor] + emoji + current[cursor:]
        )

        self.input.setCursorPosition(
            cursor + len(emoji)
        )

        self.input.setFocus()


    def send_message(self):

        if (
            self.worker is not None
            and self.worker.isRunning()
        ):
            return

        text = self.input.text().strip()

        if not text:
            return

        self.input.clear()

        self.add_user_message(text)

        self.send_button.setEnabled(False)
        self.new_button.setEnabled(False)
        self.voice_button.setEnabled(False)

        self.thinking.setText(
            "●  CONNY IS THINKING..."
        )

        self.worker = BrainWorker(text)

        self.worker.finished.connect(
            self.on_response
        )

        self.worker.failed.connect(
            self.on_error
        )

        self.worker.finished.connect(
            self.cleanup_worker
        )

        self.worker.failed.connect(
            self.cleanup_worker
        )

        self.worker.start()

    def _conny_scroll_to_bottom_now(self):
        try:
            from PyQt6.QtWidgets import QScrollArea
            from PyQt6.QtCore import QTimer

            areas = self.findChildren(QScrollArea)

            for area in areas:
                bar = area.verticalScrollBar()
                QTimer.singleShot(
                    0,
                    lambda b=bar: b.setValue(b.maximum())
                )
        except Exception:
            pass

    def _conny_final_scroll_bottom(self):
        try:
            from PyQt6.QtWidgets import QScrollArea
            from PyQt6.QtCore import QTimer

            areas = self.findChildren(QScrollArea)

            for area in areas:
                bar = area.verticalScrollBar()

                QTimer.singleShot(
                    0,
                    lambda b=bar: b.setValue(
                        b.maximum()
                    )
                )
        except Exception:
            pass

    def on_response(self, text: str):

        answer = (
            text
            or
            "I received your message, "
            "but no response was returned."
        )

        self.add_conny_message(answer)
        self._conny_final_scroll_bottom()
        self._conny_scroll_to_bottom_now()

        # Automatic TTS for normal chat is intentionally disabled.
        # Answers are displayed immediately.

    def on_error(self, text: str):

        self.add_conny_message(
            f"⚠️ {text}"
        )

    def cleanup_worker(self, *_):

        self.send_button.setEnabled(True)
        self.new_button.setEnabled(True)
        self.voice_button.setEnabled(True)

        self.thinking.setText(
            "●  CONNY READY"
        )

        self.input.setFocus()

        if self.worker is not None:
            self.worker.deleteLater()
            self.worker = None

    # ========================================================
    # SETTINGS / APPEARANCE
    # ========================================================

    def show_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("CONNY AI V13 — Settings")
        dialog.setMinimumWidth(420)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("Appearance")
        title.setStyleSheet(
            "font-size: 20px; font-weight: 900;"
        )
        layout.addWidget(title)

        description = QLabel(
            "Choose how CONNY AI V13 should look."
        )
        description.setStyleSheet(
            "color: #8b95a5;"
        )
        layout.addWidget(description)

        group = QGroupBox("Theme")
        group_layout = QVBoxLayout(group)
        group_layout.setSpacing(10)

        light = QRadioButton("☀  Light Mode")
        dark = QRadioButton("🌙  Dark Mode")

        current = self.theme_manager.current_theme()

        if current == "light":
            light.setChecked(True)
        else:
            dark.setChecked(True)

        group_layout.addWidget(light)
        group_layout.addWidget(dark)

        layout.addWidget(group)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Close
        )
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        def apply_light():
            self.theme_manager.set_theme("light")

        def apply_dark():
            self.theme_manager.set_theme("dark")

        light.toggled.connect(
            lambda checked: apply_light()
            if checked else None
        )

        dark.toggled.connect(
            lambda checked: apply_dark()
            if checked else None
        )

        dialog.exec()

    # ========================================================
    # NEW CHAT
    # ========================================================

    def new_chat(self):

        while self.chat_layout.count() > 1:

            item = self.chat_layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self.add_conny_message(
            "New conversation started. 👑 "
            "What shall we work on?"
        )

        self.input.clear()
        self.input.setFocus()

    # ========================================================
    # VOICE
    # ========================================================


    def _conny_speak_latest_response(self):
        """Speak the latest assistant response manually."""
        try:
            text = getattr(self, "_conny_latest_response_text", "")
            if not text:
                print("V13 voice: no response available to read.")
                return
            self._conny_voice_speak(text)
        except Exception as exc:
            print("V13 manual voice error:", exc)

    def _conny_voice_speak(self, text):

        if not text:
            return

        try:
            self._voice_engine.speak(text)
        except Exception as exc:
            print(
                f"CONNY VOICE OUTPUT ERROR: {exc}"
            )

    def _conny_voice_process_text(self, text):

        if not text:
            return None

        try:

            response = (
                self._voice_bridge.process_text(
                    text
                )
            )

            if response is None:
                return None

            if hasattr(response, "text"):
                answer = response.text
            else:
                answer = str(response)

            if answer:
                pass
                # V13: automatic voice playback disabled after voice input.

            return answer

        except Exception as exc:

            print(
                f"CONNY VOICE BRIDGE ERROR: {exc}"
            )

            return None

    def conny_voice_listen(self):

        if self._voice_busy:
            return

        self._voice_busy = True

        self.voice_button.setEnabled(False)

        self.thinking.setText(
            "●  LISTENING..."
        )

        try:

            text = self._voice_engine.listen()

            if not text:
                self.thinking.setText(
                    "●  CONNY READY"
                )
                return

            print(
                f"CONNY VOICE INPUT: {text}"
            )

            self.add_user_message(text)

            answer = (
                self._conny_voice_process_text(
                    text
                )
            )

            if answer:
                self.add_conny_message(
                    answer
                )

        except Exception as exc:

            print(
                f"CONNY VOICE INPUT ERROR: {exc}"
            )

            self.add_conny_message(
                f"⚠️ Voice error: {exc}"
            )

        finally:

            self._voice_busy = False
            self.voice_button.setEnabled(True)

            self.thinking.setText(
                "●  CONNY READY"
            )


def create_application():

    app = QApplication.instance()

    if app is None:
        app = QApplication(sys.argv)

    app.setApplicationName(
        "CONNY AI V13"
    )

    app.setOrganizationName(
        "Gwaneza Corneille Karenzi"
    )

    font = QFont("Sans Serif")
    font.setPointSize(10)
    app.setFont(font)

    app.setStyleSheet(
        """
        /* =================================================
           CONNY AI V13 — STAGE 9.8
           Reference-inspired desktop interface
           ================================================= */

        QWidget {
            font-family: Sans Serif;
        }

        #root {
            background: transparent;
        }

        #sidebar {
            background: rgba(7, 10, 16, 245);
            border-right: 1px solid #202631;
        }

        #sidebarCompass {
            color: #ffffff;
            font-size: 27px;
            font-weight: 900;
        }

        #sidebarBrand {
            color: #ffffff;
            font-size: 20px;
            font-weight: 900;
            letter-spacing: 1px;
        }

        #sidebarCreator {
            color: #687383;
            font-size: 9px;
            padding-left: 37px;
        }

        #sidebarLine {
            color: #202631;
            background: #202631;
            max-height: 1px;
        }

        #sidebarButton,
        #sidebarButtonActive {
            text-align: left;
            min-height: 43px;
            border-radius: 9px;
            padding-left: 10px;
            padding-right: 10px;
            border: 1px solid transparent;
            font-size: 12px;
            font-weight: 700;
        }

        #sidebarButton {
            background: transparent;
            color: #8993a2;
        }

        #sidebarButton:hover {
            background: #141922;
            color: #ffffff;
            border: 1px solid #242b37;
        }

        #sidebarButtonActive {
            background: #1b2029;
            color: #ffffff;
            border: 1px solid #303744;
        }

        #sidebarStatus {
            color: #7ee787;
            font-size: 9px;
            font-weight: 800;
            padding: 7px;
        }

        #mainPanel {
            background: transparent;
        }

        #header {
            background: rgba(9, 12, 18, 232);
            border-bottom: 1px solid #202631;
        }

        #mainTitle {
            color: #ffffff;
            font-size: 25px;
            font-weight: 900;
            letter-spacing: 1px;
        }

        #mainSubtitle {
            color: #727d8d;
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 2px;
        }

        #chatScroll {
            border: none;
            background: #000000;
        }

        #chatScroll QWidget {
            background: #000000;
        }

        #chatScroll QScrollBar:vertical {
            background: transparent;
            width: 9px;
            margin: 4px 2px 4px 0;
        }

        #chatScroll QScrollBar::handle:vertical {
            background: #343b48;
            border-radius: 4px;
            min-height: 35px;
        }

        #chatScroll QScrollBar::handle:vertical:hover {
            background: #4b5565;
        }

        #chatScroll QScrollBar::add-line:vertical,
        #chatScroll QScrollBar::sub-line:vertical {
            height: 0px;
        }

        #userBubble {
            background: rgba(31, 36, 46, 238);
            border: 1px solid #343b47;
            border-radius: 15px;
            max-width: 680px;
        }

        #connyBubble {
            background-color: #171717;
            color: #ffffff;
            border: 2px solid #3a3a3a;
            border-radius: 18px;
            padding: 8px;
            max-width: 740px;
            min-width: 180px;
        }

        #bubbleSender {
            color: #858f9e;
            font-size: 9px;
            font-weight: 900;
            letter-spacing: 1.4px;
        }

        #bubbleText {
            color: #ffffff;
            background: transparent;
            font-size: 15px;
            line-height: 1.45;
        }

        #thinking {
            color: #687383;
            background: rgba(7, 10, 16, 210);
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 1.5px;
            padding: 5px;
        }

        #composerOuter {
            background: rgba(8, 11, 17, 244);
            border-top: 1px solid #202631;
        }

        #messageInput {
            background: #11161f;
            color: #f5f7fa;
            border: 1px solid #303744;
            border-radius: 12px;
            padding: 12px 15px;
            font-size: 13px;
            min-height: 22px;
        }

        #messageInput:focus {
            border: 1px solid #596474;
            background: #141922;
        }

        #messageInput::placeholder {
            color: #626d7c;
        }

        #composerIcon,
        #secondaryButton,
        #sendButton {
            min-height: 43px;
            max-height: 43px;
            border-radius: 11px;
            font-weight: 900;
        }

        #composerIcon {
            min-width: 43px;
            max-width: 43px;
            padding: 0px;
            background: #151a23;
            color: #9ba5b4;
            border: 1px solid #303744;
            font-size: 17px;
        }

        #composerIcon:hover {
            background: #202631;
            color: #ffffff;
        }

        #secondaryButton {
            background: #151a23;
            color: #aab3c0;
            border: 1px solid #303744;
            padding-left: 14px;
            padding-right: 14px;
        }

        #secondaryButton:hover {
            background: #202631;
            color: #ffffff;
        }

        #sendButton {
            min-width: 45px;
            max-width: 45px;
            padding: 0px;
            background: #e8ebef;
            color: #0a0d12;
            border: none;
            font-size: 21px;
        }

        #sendButton:hover {
            background: #ffffff;
        }

        #sendButton:disabled {
            background: #303744;
            color: #737e8d;
        }

        #footer {
            background: rgba(6, 9, 14, 250);
            border-top: 1px solid #1d232d;
            min-height: 27px;
            max-height: 27px;
        }

        #footerStatusOnline {
            color: #7ee787;
            font-size: 9px;
            font-weight: 800;
        }

        #footerVersion {
            color: #596474;
            font-size: 8px;
            font-weight: 700;
            letter-spacing: 1px;
        }
        """
    )

    return app


def main():

    app = create_application()

    window = ConnyDesktopWindow()

    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

