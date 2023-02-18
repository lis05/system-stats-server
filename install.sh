#!/bin/bash
python3 -m pip install psutil pid

python3 replace-tokens.py system-stats-server.service
sudo cp system-stats-server.service.correct /etc/systemd/system/system-stats-server.service
sudo systemctl enable system-stats-server
sudo systemctl start system-stats-server
