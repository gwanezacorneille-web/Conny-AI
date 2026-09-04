from pathlib import Path

from PyQt6.QtCore import QObject, QEvent, Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QAbstractScrollArea,
)


ASSETS = Path(__file__).resolve().parent / "assets"

BACKGROUND = ASSETS / "conny_official_background.png"
ICON = ASSETS / "conny_compass_dark.png"


class _BackgroundController(QObject):

    def __init__(self, host, label):
        super().__init__(host)

        self.host = host
        self.label = label

        host.installEventFilter(self)

        self.update_background()

    def eventFilter(self, obj, event):

        if (
            obj is self.host
            and event.type() == QEvent.Type.Resize
        ):
            self.update_background()

        return False

    def update_background(self):

        if (
            self.host.width() <= 0
            or self.host.height() <= 0
        ):
            return

        pixmap = QPixmap(
            str(BACKGROUND)
        )

        if pixmap.isNull():
            return

        scaled = pixmap.scaled(
            self.host.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )

        self.label.setGeometry(
            self.host.rect()
        )

        self.label.setPixmap(
            scaled
        )


def apply_conny_visual_theme(window):

    app = QApplication.instance()

    # ========================================================
    # ICON
    # ========================================================

    if ICON.exists():

        icon = QIcon(
            str(ICON)
        )

        app.setWindowIcon(icon)
        window.setWindowIcon(icon)

    # ========================================================
    # BACKGROUND
    # ========================================================

    if not BACKGROUND.exists():
        return

    host = window.centralWidget()

    if host is None:
        host = window

    if not host.objectName():
        host.setObjectName(
            "connyVisualHost"
        )

    host.setAttribute(
        Qt.WidgetAttribute.WA_TranslucentBackground,
        True,
    )

    # IMPORTANT:
    # The GUI itself stays transparent so the
    # cosmic CONNY background can remain visible.

    host.setStyleSheet(
        host.styleSheet()
        + """
        QWidget#connyVisualHost {
            background: transparent;
        }
        """
    )

    background = QLabel(host)

    background.setObjectName(
        "connyChatBackground"
    )

    background.setAttribute(
        Qt.WidgetAttribute.WA_TransparentForMouseEvents,
        True,
    )

    background.setStyleSheet(
        """
        QLabel#connyChatBackground {
            background: transparent;
            border: none;
        }
        """
    )

    background.lower()

    controller = _BackgroundController(
        host,
        background,
    )

    host._conny_background_controller = controller
    host._conny_background_label = background

    for widget in host.findChildren(
        QAbstractScrollArea
    ):

        viewport = widget.viewport()

        if viewport is not None:

            viewport.setStyleSheet(
                viewport.styleSheet()
                + """
                background: transparent;
                border: none;
                """
            )
