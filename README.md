# Sentigee Web Interface

A web interface for Sentigee mail relay with Microsoft 365 OAuth2 integration. This application provides a modular interface for configuring and managing mail relay functionality using Microsoft 365 services.

## Features

- **Mail Relay**: Configure and manage mail relay with Microsoft 365 OAuth2 authentication
- **System Configuration**: Manage network settings, NTP configuration, and more
- **Additional Features**: Add and configure additional services (DDNS, NTP Server, VPN)
- **Tools**: Network diagnostic tools (ping, traceroute, DNS lookup, port scan)
- **Logs**: View mail and system logs with filtering options
- **Backup Configuration**: Schedule backups and manage backup/restore operations

## IIS6-like Mail Relay Structure

This project emulates the IIS6 mail relay folder structure:

- **Pickup**: For email messages that need to be processed immediately
- **Queue**: Holds emails waiting to be sent
- **Badmail**: Stores undeliverable emails after retry attempts
- **Drop**: Contains emails delivered locally
- **Logs**: Stores log files for email relay activity

## Installation and Setup

### Prerequisites

- Ubuntu 22.04 or later
- Python 3.8+
- pip
- Git

### Steps to Install

1. Clone this repository:
   ```
   git clone https://github.com/Frimpe01/sentigee-web-interface.git
   cd sentigee-web-interface
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:
   ```
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your_secret_key_here
   M365_CLIENT_ID=your_azure_app_client_id
   M365_CLIENT_SECRET=your_azure_app_client_secret
   M365_TENANT_ID=your_azure_tenant_id
   ```

5. Create necessary directories:
   ```
   mkdir -p opt/sentigee/logs
   mkdir -p opt/sentigee/config
   mkdir -p opt/sentigee/EmailRelay/Pickup
   mkdir -p opt/sentigee/EmailRelay/Queue
   mkdir -p opt/sentigee/EmailRelay/Badmail
   mkdir -p opt/sentigee/EmailRelay/Drop
   mkdir -p opt/sentigee/EmailRelay/Logs
   ```

6. Run the application:
   ```
   flask run --host=0.0.0.0 --port=8080
   ```

### Production Deployment with Gunicorn

For production environments, use Gunicorn as the WSGI server:

1. Install Gunicorn:
   ```
   pip install gunicorn
   ```

2. Create a systemd service file at `/etc/systemd/system/sentigee.service`:
   ```
   [Unit]
   Description=Sentigee Web Interface
   After=network.target

   [Service]
   User=your_user
   WorkingDirectory=/path/to/sentigee-web-interface
   ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8080 app:app
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```
   sudo systemctl enable sentigee
   sudo systemctl start sentigee
   ```

## Microsoft 365 Integration

To use the mail relay feature, you'll need to register an application in the Azure portal:

1. Go to the [Azure Portal](https://portal.azure.com)
2. Navigate to Azure Active Directory → App registrations → New registration
3. Name your application (e.g., "Sentigee Mail Relay")
4. Set the redirect URI to `http://your-sentigee-device:8080/oauth/callback`
5. Grant the application the following permissions:
   - Microsoft Graph: SMTP.Send
   - Office 365 Exchange Online: SMTP.Send
6. Update your `.env` file with the Client ID, Client Secret, and Tenant ID

## Development

The project uses:
- Flask backend with modular blueprints
- Tailwind CSS for styling
- Alpine.js for client-side interactivity

### Project Structure

```
sentigee-web-interface/
├── app.py                  # Main Flask application
├── routes/                 # Route blueprints
├── templates/              # HTML templates
├── static/                 # Static assets (CSS, JS)
├── utils/                  # Utility functions
├── opt/                    # Application data
│   └── sentigee/
│       ├── config/         # Configuration files
│       ├── logs/           # Application logs
│       └── EmailRelay/     # Mail relay directories
└── requirements.txt        # Python dependencies
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
