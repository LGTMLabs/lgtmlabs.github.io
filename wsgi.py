def application(env, start_response):
    """
    Simple WSGI application for LGTM Labs
    Redirects root to /static/index.html
    Apache serves everything in /static/ directly
    """
    path = env.get('PATH_INFO', '/')
    
    # For root path, redirect to static index
    if path == '/' or path == '':
        start_response('301 Moved Permanently', [
            ('Location', '/static/index.html'),
            ('Content-Type', 'text/html')
        ])
        return [b'<html><body>Redirecting to <a href="/static/index.html">LGTM Labs</a></body></html>']
    
    # For any non-static path, also redirect to static index
    # This handles SPA-like behavior
    if not path.startswith('/static/') and not path.startswith('/media/'):
        start_response('301 Moved Permanently', [
            ('Location', '/static/index.html'),
            ('Content-Type', 'text/html')
        ])
        return [b'<html><body>Redirecting to <a href="/static/index.html">LGTM Labs</a></body></html>']
    
    # If we get here, it's a /static/ or /media/ path
    # Apache should handle these directly, so this is a fallback
    start_response('404 Not Found', [('Content-Type', 'text/html')])
    return [b'<html><body>Not Found</body></html>']