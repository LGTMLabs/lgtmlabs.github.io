#!/usr/bin/env python
"""
Flask application for LGTM Labs
Serves static files with proper routing
"""
from flask import Flask, send_from_directory, redirect
import os

# Create Flask app
app = Flask(__name__)

# Get the directory where this file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

@app.route('/')
def index():
    """Serve the main index.html file"""
    return send_from_directory(STATIC_DIR, 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files from /static/ directory"""
    return send_from_directory(STATIC_DIR, path)

@app.route('/<path:path>')
def catch_all(path):
    """Catch all other routes and try to serve from static"""
    # Check if file exists in static directory
    file_path = os.path.join(STATIC_DIR, path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(STATIC_DIR, path)
    # Otherwise redirect to index
    return redirect('/')

# WSGI application object for Gandi
application = app

# For local testing
if __name__ == '__main__':
    app.run(debug=True, port=8000)