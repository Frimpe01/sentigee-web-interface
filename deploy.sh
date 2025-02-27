#!/bin/bash

# Sentigee Mail Relay System Deployment Script
# This script automates the installation and configuration of the Sentigee mail relay system

# Exit on error
set -e

# Function to display status messages
show_status() {
    echo -e "\n\033[1;34m>>> $1\033[0m"
}

# Check if script is run as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root" >&2
    exit 1
fi

# Welcome message
show_status "Welcome to Sentigee Mail Relay System Installer"
echo "This script will install and configure the Sentigee mail relay system with Microsoft 365 OAuth2 integration."
echo "Press Enter to continue or Ctrl+C to abort..."
read -r

# Collect configuration information
show_status "Collecting configuration information"

# Installation directory
INSTALL_DIR="/opt/sentigee"
echo -n "Installation directory [$INSTALL_DIR]: "
read -r input
if [ -n "$input" ]; then
    INSTALL_DIR="$input"
fi

# Web interface port
PORT="8080"
echo -n "Web interface port [$PORT]: "
read -r input
if [ -n "$input" ]; then
    PORT="$input"
fi

# Username for running the service
USERNAME="sentigee"
echo -n "Username for running the service [$USERNAME]: "
read -r input
if [ -n "$input" ]; then
    USERNAME="$input"
fi

# Microsoft 365 integration
echo -n "Microsoft 365 Client ID: "
read -r M365_CLIENT_ID

echo -n "Microsoft 365 Client Secret: "
read -r M365_CLIENT_SECRET

echo -n "Microsoft 365 Tenant ID: "
read -r M365_TENANT_ID

# Generate a random secret key
SECRET_KEY=$(openssl rand -hex 24)

# Update system and install dependencies
show_status "Updating system and installing dependencies"
apt-get update
apt-get upgrade -y
apt-get install -y python3 python3-pip python3-venv git nginx

# Create user if it doesn't exist
show_status "Setting up user account"
if ! id "$USERNAME" &>/dev/null; then
    useradd -m -s /bin/bash "$USERNAME"
    echo "User $USERNAME created"
else
    echo "User $USERNAME already exists"
fi

# Create the installation directory
show_status "Creating installation directory structure"
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/logs"
mkdir -p "$INSTALL_DIR/config"
mkdir -p "$INSTALL_DIR/EmailRelay/Pickup"
mkdir -p "$INSTALL_DIR/EmailRelay/Queue"
mkdir -p "$INSTALL_DIR/EmailRelay/Badmail"
mkdir -p "$INSTALL_DIR/EmailRelay/Drop"
mkdir -p "$INSTALL_DIR/EmailRelay/Logs"

# Clone the repository
show_status "Cloning the Sentigee repository"
cd /tmp
if [ -d "sentigee-web-interface" ]; then
    rm -rf sentigee-web-interface
fi
git clone https://github.com/Frimpe01/sentigee-web-interface.git
cd sentigee-web-interface

# Set up virtual environment and install dependencies
show_status "Setting up Python virtual environment"
python3 -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Create .env file with configuration
show_status "Configuring environment variables"
cat > "$INSTALL_DIR/.env" << EOF
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=$SECRET_KEY
M365_CLIENT_ID=$M365_CLIENT_ID
M365_CLIENT_SECRET=$M365_CLIENT_SECRET
M365_TENANT_ID=$M365_TENANT_ID
EOF

# Copy application files
show_status "Copying application files"
cp -r * "$INSTALL_DIR/"
cp -r .env "$INSTALL_DIR/"

# Create systemd service file
show_status "Creating systemd service"
cat > /etc/systemd/system/sentigee.service << EOF
[Unit]
Description=Sentigee Web Interface
After=network.target

[Service]
User=$USERNAME
WorkingDirectory=$INSTALL_DIR
ExecStart=$INSTALL_DIR/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:$PORT app:app
Restart=always
Environment="PATH=$INSTALL_DIR/venv/bin"
EnvironmentFile=$INSTALL_DIR/.env

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx as a reverse proxy
show_status "Configuring Nginx as a reverse proxy"
cat > /etc/nginx/sites-available/sentigee << EOF
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:$PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Enable the Nginx site
if [ -f /etc/nginx/sites-enabled/default ]; then
    rm /etc/nginx/sites-enabled/default
fi
ln -sf /etc/nginx/sites-available/sentigee /etc/nginx/sites-enabled/

# Set proper permissions
show_status "Setting file permissions"
chown -R "$USERNAME:$USERNAME" "$INSTALL_DIR"
chmod -R 750 "$INSTALL_DIR"

# Reload systemd, enable and start services
show_status "Starting the service"
systemctl daemon-reload
systemctl enable sentigee.service
systemctl start sentigee.service
systemctl restart nginx

# Verify the service is running
if systemctl is-active --quiet sentigee.service; then
    show_status "Installation Complete!"
    echo "The Sentigee mail relay system has been successfully installed and started."
    echo
    echo "You can access the web interface at:"
    echo "http://$(hostname -I | awk '{print $1}'):80"
    echo
    echo "Additional information:"
    echo "- Configuration files are located in $INSTALL_DIR/config"
    echo "- Log files are located in $INSTALL_DIR/logs"
    echo "- Mail relay directories are in $INSTALL_DIR/EmailRelay"
    echo
    echo "To check the service status, run: sudo systemctl status sentigee"
    echo "To view logs, run: sudo journalctl -u sentigee"
    echo
    echo "Thank you for installing Sentigee Mail Relay System!"
else
    show_status "Installation Failed"
    echo "The Sentigee service failed to start. Please check the logs with:"
    echo "sudo journalctl -u sentigee"
fi
