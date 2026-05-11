#!/bin/sh

echo "Installing PGR Tools..."

# Update system packages (recommended)
sudo apt update

# Install dependencies
sudo apt install ffmpeg -y
sudo apt install python3 -y
sudo apt install python3-pip -y

# Install Python libraries
pip3 install yt-dlp colorama pyfiglet

# Install pgr command
chmod 755 pgr
sudo mv pgr /usr/local/bin/
chmod 755 /usr/local/bin/pgr

echo "Installed! Type: pgr"
