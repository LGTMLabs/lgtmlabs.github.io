<?php
// Simple router for LGTM Labs static site
// This file ensures compatibility with Gandi's PHP hosting

// Get the requested URI
$request_uri = $_SERVER['REQUEST_URI'];

// Remove query string if present
$request_uri = strtok($request_uri, '?');

// Default to index.html
if ($request_uri == '/' || $request_uri == '') {
    $file = 'index.html';
} else {
    // Remove leading slash
    $file = ltrim($request_uri, '/');
}

// Security: Prevent directory traversal
$file = str_replace('..', '', $file);
$file = str_replace('//', '/', $file);

// Check if file exists
if (file_exists($file) && is_file($file)) {
    // Determine content type
    $ext = pathinfo($file, PATHINFO_EXTENSION);
    switch ($ext) {
        case 'html':
            header('Content-Type: text/html');
            break;
        case 'css':
            header('Content-Type: text/css');
            break;
        case 'js':
            header('Content-Type: application/javascript');
            break;
        case 'svg':
            header('Content-Type: image/svg+xml');
            break;
        default:
            header('Content-Type: application/octet-stream');
    }
    
    // Serve the file
    readfile($file);
} else {
    // Fallback to index.html for SPA behavior
    header('Content-Type: text/html');
    readfile('index.html');
}
?>