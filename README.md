# Sentigee Web Interface

A web interface for Sentigee mail relay with Microsoft 365 OAuth2 integration. This application provides a modular interface for configuring and managing mail relay functionality using Microsoft 365 services.

## Features

- Mail Relay Configuration
- System Configuration
- Additional Features
- Tools
- Logs
- Backup Configuration

## IIS6-like Mail Relay Structure

This project emulates the IIS6 mail relay folder structure:

- Pickup: For email messages that need to be processed immediately
- Queue: Holds emails waiting to be sent
- Badmail: Stores undeliverable emails after retry attempts
- Drop: Contains emails delivered locally
- Logs: Stores log files for email relay activity

## Installation and Setup

1. Clone this repository
2. Install requirements: `pip install -r requirements.txt`
3. Run the application: `python app.py`

## Development

The project uses a Flask backend with Tailwind CSS for styling the frontend.