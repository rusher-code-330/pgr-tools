@echo off

echo Installing PGR Tools...

:: Install Python packages
pip install yt-dlp colorama pyfiglet

echo.
echo NOTE: ffmpeg must be installed manually on Windows
echo You can install it via: winget install Gyan.FFmpeg
echo.

echo Setting up PGR command...

:: Create pgr launcher
echo @echo off > pgr.bat
echo python %%USERPROFILE%%\pgr-tools\pgr.py %%* >> pgr.bat

:: Move to PATH (Windows system folder)
move pgr.bat C:\Windows\System32\

echo.
echo Installed! Type: pgr
pause
