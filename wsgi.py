#!/usr/bin/env python
"""
WSGI application for LGTM Labs - serves static files from /static/ directory
Compatible with Gandi web hosting
"""
import os
import mimetypes

def application(environ, start_response):
    """
    WSGI application that serves static files.
    Gandi automatically serves /static/ and /media/ directories,
    but we'll handle root requests to redirect to static files.
    """
    
    # Get the request path
    path = environ.get('PATH_INFO', '/')
    
    # For root path, redirect to the static index.html
    if path == '/' or path == '':
        # Redirect to /static/index.html
        start_response('301 Moved Permanently', [
            ('Location', '/static/index.html'),
            ('Content-Type', 'text/html')
        ])
        return [b'<html><body><a href="/static/index.html">Redirecting...</a></body></html>']
    
    # For any other path, try to serve from static
    if not path.startswith('/static/'):
        # Redirect to static version
        redirect_path = '/static' + path
        start_response('301 Moved Permanently', [
            ('Location', redirect_path),
            ('Content-Type', 'text/html')
        ])
        return [b'<html><body>Redirecting to static files...</body></html>']
    
    # Let Gandi's server handle static files directly
    # This should not be reached as Gandi serves /static/ automatically
    start_response('404 Not Found', [('Content-Type', 'text/plain')])
    return [b'File not found. Static files should be accessed via /static/ path.']