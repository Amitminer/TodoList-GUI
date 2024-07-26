@echo off
setlocal

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python and try again.
    exit /b 1
)

:: Install requirements
echo Installing required packages...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Failed to install requirements. Please check the requirements file.
    exit /b 1
)

:: Build the executable using PyInstaller
echo Building the executable...
pyinstaller --onefile src/main.py
if %ERRORLEVEL% neq 0 (
    echo Failed to build the executable. Please check the PyInstaller command and script.
    exit /b 1
)

:: Provide feedback on the location of the executable
echo Build completed successfully.
echo The executable file is located at dist\main.exe

endlocal
pause
