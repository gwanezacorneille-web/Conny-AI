@echo off
setlocal

cd /d "%~dp0"

echo ============================================================
echo CONNY AI V13 - WINDOWS BUILD
echo ============================================================

if not exist ".venv\Scripts\python.exe" (
    echo Creating Windows virtual environment...
    python -m venv .venv
)

echo.
echo Installing/updating dependencies...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements-windows.txt

echo.
echo Cleaning previous build...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

echo.
echo Building CONNY AI from Windows spec...
".venv\Scripts\python.exe" -m PyInstaller ^
    --clean ^
    --noconfirm ^
    CONNY-WINDOWS.spec

echo.
if exist "dist\CONNY AI\CONNY AI.exe" (
    echo ============================================================
    echo BUILD SUCCESS
    echo ============================================================
    echo.
    echo Executable:
    echo dist\CONNY AI\CONNY AI.exe
) else (
    echo ============================================================
    echo BUILD FAILED
    echo ============================================================
)

echo.
pause
endlocal
