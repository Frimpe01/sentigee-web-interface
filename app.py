from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, url_for
import os
import logging
import json
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Main routes
@app.route('/')
def index():
    logger.debug("Serving mail relay page")
    return render_template('mail_relay.html', active_tab='mail_relay')

@app.route('/system')
def system():
    logger.debug("Serving system configuration page")
    return render_template('system_config.html', active_tab='system')

@app.route('/features')
def features():
    logger.debug("Serving additional features page")
    return render_template('features.html', active_tab='features')

@app.route('/tools')
def tools():
    logger.debug("Serving tools page")
    return render_template('tools.html', active_tab='tools')

@app.route('/logs')
def logs():
    logger.debug("Serving logs page")
    return render_template('logs.html', active_tab='logs')

@app.route('/backup')
def backup():
    logger.debug("Serving backup configuration page")
    return render_template('backup.html', active_tab='backup')

@app.route('/static/<path:filename>')
def serve_static(filename):
    logger.debug(f"Serving static file: {filename}")
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Flask server is running"})

# API Routes for mail relay
@app.route('/api/mail-relay/status', methods=['GET'])
def mail_relay_status():
    """Get the current status of the mail relay"""
    try:
        # Check token status (mocked for now)
        token_status = {
            'valid': False,
            'last_refreshed': None,
            'last_attempt': None,
            'next_attempt': None,
            'result': 'Not configured',
            'user': None
        }
        
        # In production, we would check if oauth_token.json exists
        config_dir = os.path.join('opt', 'sentigee', 'config')
        token_file = os.path.join(config_dir, 'oauth_token.json')
        
        # Mock internet connectivity check
        internet_connected = True
        
        return jsonify({
            'internet_connected': internet_connected,
            'token_status': token_status,
            'mail_relay_configured': False
        })
    except Exception as e:
        logger.error(f"Error getting mail relay status: {str(e)}")
        return jsonify({
            'error': f"Error getting mail relay status: {str(e)}"
        }), 500

@app.route('/api/mail-relay/configure', methods=['POST'])
def configure_mail_relay():
    """Configure the mail relay with Microsoft 365 credentials"""
    try:
        data = request.json
        email = data.get('email')
        shared_mailbox = data.get('shared_mailbox')
        use_alias = data.get('use_alias')
        alias = data.get('alias')
        
        # In production, we would save this configuration
        # and redirect to Microsoft OAuth
        
        return jsonify({
            'success': True,
            'message': 'Configuration saved, redirecting to Microsoft for authentication'
        })
    except Exception as e:
        logger.error(f"Error configuring mail relay: {str(e)}")
        return jsonify({
            'success': False,
            'error': f"Error configuring mail relay: {str(e)}"
        }), 500

# Ensure required directories exist
def ensure_directories():
    required_dirs = [
        os.path.join('opt', 'sentigee', 'logs'),
        os.path.join('opt', 'sentigee', 'config'),
        os.path.join('opt', 'sentigee', 'EmailRelay', 'Pickup'),
        os.path.join('opt', 'sentigee', 'EmailRelay', 'Queue'),
        os.path.join('opt', 'sentigee', 'EmailRelay', 'Badmail'),
        os.path.join('opt', 'sentigee', 'EmailRelay', 'Drop'),
        os.path.join('opt', 'sentigee', 'EmailRelay', 'Logs'),
    ]
    
    for directory in required_dirs:
        os.makedirs(directory, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")

if __name__ == '__main__':
    ensure_directories()
    app.run(host='0.0.0.0', port=8080, debug=True)