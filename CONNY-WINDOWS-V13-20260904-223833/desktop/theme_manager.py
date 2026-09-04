from __future__ import annotations

from pathlib import Path
from PyQt6.QtCore import QSettings


DARK_THEME = """
QWidget {
    color: #eef1f5;
}

#sidebar {
    background: rgba(7, 10, 16, 245);
}

#mainPanel {
    background: transparent;
}

#header {
    background: rgba(9, 12, 18, 232);
}

#messageInput {
    background: #11161f;
    color: #f5f7fa;
}

#composerOuter {
    background: rgba(8, 11, 17, 244);
}

#footer {
    background: rgba(6, 9, 14, 250);
}
"""


LIGHT_THEME = """
QWidget {
    color: #20242b;
}

#sidebar {
    background: rgba(245, 247, 250, 245);
    border-right: 1px solid #d8dde5;
}

#sidebarCompass {
    color: #20242b;
}

#sidebarBrand {
    color: #20242b;
}

#sidebarCreator {
    color: #667085;
}

#sidebarLine {
    color: #d8dde5;
    background: #d8dde5;
}

#sidebarButton {
    color: #667085;
}

#sidebarButton:hover {
    background: #e9edf2;
    color: #20242b;
}

#sidebarButtonActive {
    background: #e1e6ed;
    color: #20242b;
    border: 1px solid #cbd2dc;
}

#mainPanel {
    background: transparent;
}

#header {
    background: rgba(248, 249, 251, 232);
    border-bottom: 1px solid #d8dde5;
}

#mainTitle {
    color: #20242b;
}

#mainSubtitle {
    color: #667085;
}

#userBubble {
    background: rgba(235, 239, 244, 238);
    border: 1px solid #d5dae2;
}

#connyBubble {
    background: rgba(248, 249, 251, 235);
    border: 1px solid #d5dae2;
}

#bubbleSender {
    color: #667085;
}

#bubbleText {
    color: #20242b;
}

#thinking {
    color: #667085;
    background: rgba(245, 247, 250, 220);
}

#composerOuter {
    background: rgba(248, 249, 251, 244);
    border-top: 1px solid #d8dde5;
}

#messageInput {
    background: #ffffff;
    color: #20242b;
    border: 1px solid #cbd2dc;
}

#messageInput:focus {
    background: #ffffff;
    border: 1px solid #8b95a5;
}

#messageInput::placeholder {
    color: #8a93a1;
}

#composerIcon,
#secondaryButton {
    background: #eef1f5;
    color: #4b5563;
    border: 1px solid #cbd2dc;
}

#composerIcon:hover,
#secondaryButton:hover {
    background: #e1e6ed;
    color: #20242b;
}

#footer {
    background: rgba(242, 244, 247, 250);
    border-top: 1px solid #d8dde5;
}

#footerVersion {
    color: #667085;
}
"""


class ThemeManager:

    def __init__(self, app):
        self.app = app
        self.settings = QSettings(
            "Gwaneza Corneille Karenzi",
            "CONNY AI V13",
        )

    def current_theme(self):
        return self.settings.value(
            "appearance",
            "dark",
            type=str,
        )

    def set_theme(self, theme):
        if theme not in ("dark", "light"):
            theme = "dark"

        self.settings.setValue(
            "appearance",
            theme,
        )

        self.apply(theme)

    def apply(self, theme=None):
        if theme is None:
            theme = self.current_theme()

        self.app.setStyleSheet(
            self.app.styleSheet()
            + (
                DARK_THEME
                if theme == "dark"
                else LIGHT_THEME
            )
        )
