#!/data/data/com.termux/files/usr/bin/sh

echo "Installing PGR Tools..."

pkg install ffmpeg -y

pkg install python -y

pip install yt-dlp colorama pyfiglet

chmod 755 pgr
mv pgr $PREFIX/bin/
chmod 755 $PREFIX/bin/pgr

echo "Installed! Type: pgr"
