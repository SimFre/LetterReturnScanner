
Change SFTP details and serial port in the python script.

sudo cp letterreturns.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable letterreturns
sudo systemctl start letterreturns
