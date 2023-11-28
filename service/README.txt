sudo vi /etc/systemd/system/sensor.service
sudo vi /etc/systemd/system/app.service

sudo systemctl daemon-reload
sudo systemctl enable sensor.service
sudo systemctl enable app.service

sudo reboot

sudo systemctl status sensor.service
sudo systemctl status app.service