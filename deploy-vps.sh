#!/bin/bash

# VPS deployment script
echo "Setting up Legal Billing Email Summarizer on VPS..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-pip -y

# Create application directory
sudo mkdir -p /opt/legal-billing
sudo chown $USER:$USER /opt/legal-billing
cd /opt/legal-billing

# Clone repository (replace with your repo URL)
git clone https://github.com/your-username/legal-billing-summarizer.git .

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
echo "Please edit .env file with your API keys"

# Create systemd service
sudo tee /etc/systemd/system/legal-billing.service > /dev/null <<EOF
[Unit]
Description=Legal Billing Email Summarizer
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/legal-billing
Environment=PATH=/opt/legal-billing/venv/bin
ExecStart=/opt/legal-billing/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable legal-billing
sudo systemctl start legal-billing

echo "Deployment complete!"
echo "Your app should be running on port 8000"
