from __future__ import annotations

import threading

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import (
    QPushButton,
    QLabel,
    QApplication,
    QTextEdit,
    QPlainTextEdit,
    QTextBrowser,
)

import speech_recognition as sr

from .voice_bridge import ConnyVoiceBridge
from .tts import ConnyTTS


class ConnyVoiceControl(QObject):
    """
    V13 voice UI adapter.

    Pipeline:
        Microphone
            ↓
        SpeechRecognition
            ↓
        ConnyVoiceBridge
            ↓
        Real Conny Brain
            ↓
        GUI
            ↓
        espeak-ng
    """

    status_changed = pyqtSignal(str)
    text_received = pyqtSignal(str)
    response_received = pyqtSignal(str)

    def __init__(self, window=None, bridge=None):
        super().__init__(window)

        self.window = window
        self.bridge = bridge or ConnyVoiceBridge()
        self._tts = ConnyTTS()

        self.recognizer = sr.Recognizer()
        self.listening = False

        self.button = None
        self.status_label = None

        self._build_controls()

        self.status_changed.connect(self._set_status)
        self.text_received.connect(self._show_user_text)
        self.response_received.connect(self._show_response)

    # --------------------------------------------------------
    # GUI
    # --------------------------------------------------------

    def _build_controls(self):
        if self.window is None:
            return

        self.button = QPushButton("🎤 VOICE", self.window)
        self.button.setObjectName("connyVoiceButton")
        self.button.setToolTip(
            "Click to speak to Conny AI"
        )

        self.button.setMinimumHeight(36)
        self.button.clicked.connect(self.start_listening)

        self.status_label = QLabel(
            "🎙️ Voice ready",
            self.window,
        )
        self.status_label.setObjectName(
            "connyVoiceStatus"
        )

        self.status_label.setMinimumHeight(28)

        self._position_controls()

        try:
            self.window.installEventFilter(self)
        except Exception:
            pass

    def _position_controls(self):
        """
        Keep voice controls in a clean bottom-right area.

        The voice controls are deliberately positioned above the
        normal input/action controls so they do not cover NEW/SEND.
        """

        if not self.window or not self.button:
            return

        w = max(500, self.window.width())
        h = max(400, self.window.height())

        button_width = 125
        button_height = 38

        margin_right = 28
        bottom_reserved = 150

        x = w - button_width - margin_right
        y = max(30, h - bottom_reserved - button_height)

        self.button.setGeometry(
            x,
            y,
            button_width,
            button_height,
        )

        if self.status_label:
            status_width = 190
            status_height = 26

            status_x = w - status_width - margin_right
            status_y = y + button_height + 5

            self.status_label.setGeometry(
                status_x,
                status_y,
                status_width,
                status_height,
            )

        self.button.raise_()

        if self.status_label:
            self.status_label.raise_()

    def eventFilter(self, obj, event):
        try:
            from PyQt6.QtCore import QEvent

            if obj is self.window and event.type() == QEvent.Type.Resize:
                self._position_controls()
        except Exception:
            pass

        return False

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    def _set_status(self, text):
        if self.status_label:
            self.status_label.setText(text)

        if self.button:
            self.button.setEnabled(
                not self.listening
            )

    # --------------------------------------------------------
    # MICROPHONE
    # --------------------------------------------------------

    def microphone_available(self):
        try:
            names = sr.Microphone.list_microphone_names()
            return len(names) > 0
        except Exception:
            return False

    def start_listening(self):
        if self.listening:
            return

        self.listening = True

        if self.button:
            self.button.setText("🎙️ LISTENING...")

        self.status_changed.emit(
            "🎙️ Listening..."
        )

        thread = threading.Thread(
            target=self._listen_worker,
            daemon=True,
        )
        thread.start()

    def _listen_worker(self):
        try:
            with sr.Microphone() as source:
                try:
                    self.recognizer.adjust_for_ambient_noise(
                        source,
                        duration=0.4,
                    )
                except Exception:
                    pass

                audio = self.recognizer.listen(
                    source,
                    timeout=8,
                    phrase_time_limit=15,
                )

            self.status_changed.emit(
                "🧠 Understanding..."
            )

            try:
                text = self.recognizer.recognize_google(
                    audio
                )
            except sr.UnknownValueError:
                self.status_changed.emit(
                    "❓ Speech not understood"
                )
                return

            except sr.RequestError:
                self.status_changed.emit(
                    "⚠ Speech service unavailable"
                )
                return

            text = text.strip()

            if not text:
                self.status_changed.emit(
                    "🎙️ Nothing heard"
                )
                return

            self.text_received.emit(text)

            self.status_changed.emit(
                "🧠 Conny is thinking..."
            )

            result = self.bridge.process_text(text)

            response = getattr(
                result,
                "text",
                str(result),
            )

            response = str(response).strip()

            if not response:
                response = (
                    "I received your message, "
                    "but I did not get a response."
                )

            self.response_received.emit(response)

            self.status_changed.emit(
                "🔊 Speaking..."
            )

            # V13: voice input must not automatically speak the answer.
            # Playback is controlled explicitly by the desktop GUI.

            self.status_changed.emit(
                "🟢 Brain Online • Voice Ready"
            )

        except sr.WaitTimeoutError:
            self.status_changed.emit(
                "⏱️ Listening timed out"
            )

        except OSError as exc:
            self.status_changed.emit(
                "🎤 Microphone unavailable"
            )
            print(
                "Voice microphone error:",
                exc,
            )

        except Exception as exc:
            self.status_changed.emit(
                "⚠ Voice error"
            )
            print(
                "Voice pipeline error:",
                repr(exc),
            )

        finally:
            self.listening = False

            if self.button:
                self.button.setText(
                    "🎤 VOICE"
                )

                self.button.setEnabled(
                    True
                )

    # --------------------------------------------------------
    # SPEECH OUTPUT
    # --------------------------------------------------------

    def _speak(self, text):
        try:
            self._tts.speak(text)
        except Exception as exc:
            print(
                "Speech output error:",
                repr(exc),
            )

    # --------------------------------------------------------
    # GUI MESSAGE DISPLAY
    # --------------------------------------------------------

    def _find_text_widget(self):
        if not self.window:
            return None

        widgets = self.window.findChildren(
            QTextEdit
        )

        if widgets:
            return widgets[0]

        widgets = self.window.findChildren(
            QPlainTextEdit
        )

        if widgets:
            return widgets[0]

        widgets = self.window.findChildren(
            QTextBrowser
        )

        if widgets:
            return widgets[0]

        return None

    def _append_text(self, text):
        widget = self._find_text_widget()

        if widget is None:
            return

        try:
            if hasattr(widget, "append"):
                widget.append(text)
                return

            if hasattr(widget, "insertPlainText"):
                widget.insertPlainText(
                    text + "\n"
                )

        except Exception as exc:
            print(
                "GUI message error:",
                repr(exc),
            )

    def _show_user_text(self, text):
        self._append_text(
            f"You 🎤: {text}"
        )

    def _show_response(self, text):
        self._append_text(
            f"Conny AI 🤖: {text}"
        )
