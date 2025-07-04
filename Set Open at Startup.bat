@echo off
REM Set the name of your EXE
SET EXE_NAME=Spyral RAM Usage.exe

REM Set the full path to the EXE (same folder as this .bat file)
SET EXE_PATH=%~dp0%EXE_NAME%

REM Set the shortcut name and path
SET SHORTCUT_NAME=SpyralRAMUsage.lnk
SET STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
SET SHORTCUT_PATH=%STARTUP_FOLDER%\%SHORTCUT_NAME%

REM Check if the EXE exists
IF NOT EXIST "%EXE_PATH%" (
    echo EXE file not found at: %EXE_PATH%
    pause
    exit /b
)

REM Create the shortcut using PowerShell
powershell -command "$s=(New-Object -COM WScript.Shell).CreateShortcut('%SHORTCUT_PATH%'); $s.TargetPath='%EXE_PATH%'; $s.WorkingDirectory='%~dp0'; $s.Save()"

echo Shortcut created in Startup folder.
pause
