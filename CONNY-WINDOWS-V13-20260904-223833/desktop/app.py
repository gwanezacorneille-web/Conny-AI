from __future__ import annotations
from desktop.visual_theme import apply_conny_visual_theme

import sys

from PyQt6.QtWidgets import QApplication
from .main_window import create_application

from .main_window import ConnyDesktopWindow
from .voice_bridge import ConnyVoiceBridge
from .voice_control import ConnyVoiceControl


def main():
    app = create_application()

    window = ConnyDesktopWindow()

    # Preserve the existing real V13 bridge.
    bridge = ConnyVoiceBridge()

    # Attach voice to the existing desktop window.
    voice_control = ConnyVoiceControl(
        window=window,
        bridge=bridge,
    )

    # Keep a strong reference on the window.
    window.conny_voice_control = voice_control

    apply_conny_visual_theme(window)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
