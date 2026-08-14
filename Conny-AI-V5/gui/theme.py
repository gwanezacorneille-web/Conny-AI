import customtkinter as ctk


# ============================
# CONNY AI V5 THEME
# ============================

APP_NAME = "CONNY AI V5.0"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 750


# Colors

BG_COLOR = "#0F172A"
SIDEBAR_COLOR = "#111827"
CHAT_COLOR = "#1E293B"
ACCENT_COLOR = "#2563EB"
BUTTON_COLOR = "#3B82F6"
TEXT_COLOR = "#F8FAFC"
SECONDARY_TEXT = "#94A3B8"


# Fonts

TITLE_FONT = ("Arial", 24, "bold")
HEADER_FONT = ("Arial", 18, "bold")
NORMAL_FONT = ("Arial", 14)
SMALL_FONT = ("Arial", 12)


def apply_theme():

    ctk.set_appearance_mode("dark")

    ctk.set_default_color_theme("blue")
