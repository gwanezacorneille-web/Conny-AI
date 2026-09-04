from __future__ import annotations

import subprocess
import threading
from typing import Callable, Optional

import speech_recognition as sr


class ConnyVoice:
    """
    V13 voice layer.

    Speech recognition:
        microphone -> SpeechRecognition -> text

    Speech synthesis:
        text -> espeak-ng -> speaker

    The actual intelligence remains in the existing V13 bridge.
    """

    def __init__(self, language: str = "en-US"):
        self.language = language
        self.recognizer = sr.Recognizer()
        self._speaking = False
        self._lock = threading.Lock()

    def listen(self, timeout: Optional[float] = 5,
               phrase_time_limit: Optional[float] = 12) -> str:
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

        try:
            return self.recognizer.recognize_google(
                audio,
                language=self.language,
            )
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as exc:
            raise RuntimeError(
                f"Speech recognition service unavailable: {exc}"
            ) from exc

    def speak(self, text: str) -> None:
        if not text:
            return

        with self._lock:
            self._speaking = True

        try:
            subprocess.run(
                ["espeak-ng", "-s", "155", "-v", "en", text],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        finally:
            with self._lock:
                self._speaking = False

    @property
    def speaking(self) -> bool:
        with self._lock:
            return self._speaking

    def listen_async(
        self,
        on_result: Callable[[str], None],
        on_error: Optional[Callable[[Exception], None]] = None,
    ) -> threading.Thread:

        def worker():
            try:
                result = self.listen()
                on_result(result)
            except Exception as exc:
                if on_error:
                    on_error(exc)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        return thread

    def speak_async(self, text: str) -> threading.Thread:
        thread = threading.Thread(
            target=self.speak,
            args=(text,),
            daemon=True,
        )
        thread.start()
        return thread
