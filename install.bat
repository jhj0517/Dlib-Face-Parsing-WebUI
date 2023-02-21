@echo off

if not exist "%~dp0\venv\Scripts" (
    echo Creating venv...
    python -m venv venv
)

echo checked the venv folder. now installing requirements..
cd /d "%~dp0\venv\Scripts"
call activate.bat

cd /d "%~dp0"
pip install -r requirements.txt

echo.
echo Requirements installed successfully.
pause