#!/bin/bash
# setup.sh
# This script is used to set up the required external tools for the Flask application.

echo "Starting setup..."
sudo apt-get update
echo "Installing sublist3r..."
sudo apt-get install sublist3r
echo "Installing nmap..."
sudo apt-get install nmap
echo "Installing whatweb..."
sudo apt-get install whatweb

echo "Installing dirble..."
DIRBLE_URL="https://github.com/nccgroup/dirble/releases/download/v1.4.2/dirble-1.4.2-20190709-x86_64-linux.zip"
DIRBLE_ZIP="dirble.zip"
wget $DIRBLE_URL -O $DIRBLE_ZIP
unzip $DIRBLE_ZIP
chmod +x dirble
sudo mv dirble /usr/local/bin/
echo "Setup complete."

