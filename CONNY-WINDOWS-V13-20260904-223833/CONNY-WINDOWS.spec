# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules

ROOT = Path.cwd()

datas = [
    (str(ROOT / "desktop" / "assets"), "desktop/assets"),
    (str(ROOT / "database" / "conny.db"), "database"),
]

hiddenimports = []

for package in [
    "bridge",
    "core_adapter",
    "desktop",
    "shared",
]:
    try:
        hiddenimports += collect_submodules(package)
    except Exception:
        pass

a = Analysis(
    ["windows_entry.py"],
    pathex=[str(ROOT)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "android",
        "tests",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="CONNY AI",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
)
