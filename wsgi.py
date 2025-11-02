#!/usr/bin/env python
"""
Flask application for LGTM Labs
Serves static files with proper routing
Compatible with Python 3.13
"""
import os
import sys

# Ensure we can import Flask
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, send_from_directory

# Create Flask app with explicit static folder
app = Flask(__name__, static_folder='static', static_url_path='/static')

# Get the static directory path
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')

@app.route('/')
def index():
    """Serve the main index.html file"""
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    """Serve any file from static directory"""
    if os.path.exists(os.path.join(STATIC_DIR, filename)):
        return send_from_directory(STATIC_DIR, filename)
    # Fallback to index.html
    return send_from_directory(STATIC_DIR, 'index.html')

# WSGI application object for Gandi - this is what uWSGI looks for
application = app

# For local testing
if __name__ == '__main__':
    print(f"Serving static files from: {STATIC_DIR}")
    app.run(debug=True, host='0.0.0.0', port=8000)