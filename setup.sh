cd /opt/
mkdir -p katalog
cd katalog
python3 -m venv bot
wget -q https://raw.githubusercontent.com/san-labs21/katalog/main/admin.html
wget -q https://raw.githubusercontent.com/san-labs21/katalog/main/katalog.html
wget -q https://raw.githubusercontent.com/san-labs21/katalog/main/app.py

cat <<EOL > /opt/katalog/run.sh
#!/bin/bash
source /opt/bot/bin/activate
python3 /opt/katalog/app.py
EOL

# Buat file service systemd
cat <<EOF > /etc/systemd/system/katalog.service
[Unit]
Description=San Bot Manager
After=network.target

[Service]
ExecStart=/usr/bin/bash /opt/katalog/run.sh
WorkingDirectory=/opt/katalog
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd dan mulai service
systemctl daemon-reload
systemctl enable katalog
systemctl start katalog
 
 
