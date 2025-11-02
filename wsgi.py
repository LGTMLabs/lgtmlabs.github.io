#!/usr/bin/env python3
"""
Simple WSGI application to serve static files for LGTM Labs
"""
import os
import mimetypes

def application(environ, start_response):
    # Get the requested path
    path = environ.get('PATH_INFO', '/')
    
    # Default to index.html for root
    if path == '/':
        path = '/index.html'
    
    # Remove leading slash for file access
    file_path = path.lstrip('/')
    
    # Security: prevent directory traversal
    file_path = os.path.normpath(file_path)
    if '..' in file_path:
        start_response('403 Forbidden', [('Content-Type', 'text/plain')])
        return [b'Forbidden']
    
    # Check if file exists
    if os.path.isfile(file_path):
        # Guess content type
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = 'application/octet-stream'
        
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            start_response('200 OK', [
                ('Content-Type', content_type),
                ('Content-Length', str(len(content)))
            ])
            return [content]
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [b'Internal Server Error']
    else:
        # File not found
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Not Found']