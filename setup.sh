#!/bin/bash

# Create log directory
sudo mkdir -p /var/log/spectrogram
sudo chown pi:pi /var/log/spectrogram

# Copy systemd service file
sudo cp spectrogram.service /etc/systemd/system/

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable spectrogram
sudo systemctl start spectrogram

# Add user to required groups
sudo usermod -a -G audio user

echo "Setup complete! The service will start automatically on boot."

(crontab -l 2>/dev/null; echo "*/5 * * * * cd /home/spectro && git pull") | crontab - 