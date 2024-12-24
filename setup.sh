#!/bin/bash

# Install required packages
sudo apt-get update
sudo apt-get install -y git python3-pip

# Set up IQAudio DAC
echo "dtoverlay=iqaudio-dacplus" | sudo tee -a /boot/config.txt

# Create cron job for git pulls
(crontab -l 2>/dev/null; echo "*/5 * * * * cd /home/pi/audio-analyzer && git pull") | crontab - 