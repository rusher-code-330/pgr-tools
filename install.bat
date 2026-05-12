@echo off

echo Installing PGR Tools...

pip install yt-dlp colorama pyfiglet

echo Installing Node.js...
winget install OpenJS.NodeJS

echo.
echo NOTE: ffmpeg must be installed manually on Windows
echo You can install it via: winget install Gyan.FFmpeg
echo.

echo Setting up PGR command...

echo @echo off > pgr.bat
echo python %%USERPROFILE%%\pgr-tools\pgr.py %%* >> pgr.bat

move pgr.bat C:\Windows\System32\

echo.
echo Installed! Type: pgr
pause
