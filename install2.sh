#!/bin/sh

echo "Installing PGR Tools..."


sudo apt update

sudo apt install nodejs -y
sudo apt install ffmpeg -y
sudo apt install python3 -y
sudo apt install python3-pip -y


pip3 install yt-dlp colorama pyfiglet


chmod 755 pgr-linux
sudo mv pgr-linux /usr/local/bin/pgr
chmod 755 /usr/local/bin/pgr

echo "Installed! Type: pgr"
