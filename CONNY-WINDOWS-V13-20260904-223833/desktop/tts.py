from __future__ import annotations

import platform
import subprocess
import threading


class ConnyTTS:
    """
    CONNY AI V13 cross-platform speech output.

    Linux:
        espeak-ng

    Windows:
        pyttsx3 / Windows SAPI

    Speech output is manual; normal chat does not automatically speak.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._engine = None

        if platform.system() == "Windows":
            try:
                import pyttsx3

                self._engine = pyttsx3.init()
                self._engine.setProperty("rate", 155)
            except Exception as exc:
                print("CONNY Windows TTS initialization error:", repr(exc))
                self._engine = None

    def speak(self, text: str) -> None:
        if not text:
            return

        text = str(text).strip()

        if not text:
            return

        with self._lock:
            if platform.system() == "Windows":
                self._speak_windows(text)
            else:
                self._speak_linux(text)

    def _speak_linux(self, text: str) -> None:
        try:
            subprocess.run(
                [
                    "espeak-ng",
                    "-s",
                    "155",
                    "-v",
                    "en",
                    text,
                ],
                check=False,
            )
        except Exception as exc:
            print("CONNY Linux TTS error:", repr(exc))

    def _speak_windows(self, text: str) -> None:
        if self._engine is None:
            print("CONNY Windows TTS unavailable.")
            return

        try:
            self._engine.say(text[:4000])
            self._engine.runAndWait()
        except Exception as exc:
            print("CONNY Windows TTS error:", repr(exc))


__all__ = ["ConnyTTS"]
