"""
Created by CVE, 05-11-2025, together with Copilot <3

Handles API authentication for Barge Master API with Authentik OAuth2/OIDC.

Uses browser-based OAuth2 flow with PKCE. No hardcoded credentials.
Tokens are cached locally. See OAUTH2_SETUP_GUIDE.md for setup instructions.
"""

import requests
import webbrowser
import json
import os
import socket
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, urlencode
import threading
import hashlib
import base64
import secrets

CLIENT_ID = os.getenv('AUTHENTIK_CLIENT_ID', 'rit3UTLMn09UVJjgWRhRKg7bHgvTKW2fVCyWagtI')

AUTHENTIK_URL = os.getenv('AUTHENTIK_URL', 'https://auth.app.barge-master.com')

API_BASE_URL = 'https://api.app.barge-master.com'

# API_BASE_URL = 'http://localhost:8008' # for development purposes

def _get_oauth_config():
    """Fetch OAuth2 config from API server (allows updating Client ID without code changes)"""
    try:
        r = requests.get(f'{API_BASE_URL}/.well-known/oauth-config', timeout=5)
        if r.ok:
            return r.json()
    except:
        pass
    return {'client_id': CLIENT_ID, 'auth_url': AUTHENTIK_URL}

class TokenCache:
    def __init__(self):
        cache_dir = Path.home() / ".pybm"
        cache_dir.mkdir(exist_ok=True)

        self.cache_file = cache_dir / "auth_token.json"

    

    def save(self, token_data):
        with open(self.cache_file, "w") as f:
            json.dump(token_data, f, indent=2)

    

    def load(self):
        if not self.cache_file.exists():
            return None
        try:
            with open(self.cache_file, "r") as f:
                return json.load(f)
        except:
            return None

class OAuth2CallbackHandler(BaseHTTPRequestHandler):

    result = None

    

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        OAuth2CallbackHandler.result = {
            'code': params.get('code', [None])[0],
            'error': params.get('error', [None])[0],
            'error_description': params.get('error_description', [None])[0]
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        status = "Failed" if self.result.get('error') else "Successful"
        color = "red" if self.result.get('error') else "rgb(0, 173, 239)"
        msg = self.result.get('error_description', '') if self.result.get('error') else 'You can close this window'
        
        html = f'<html><body style="font-family:Arial;text-align:center;padding:50px"><h1 style="color:{color}">BM-API Authentication {status}</h1><p>{msg}</p></body></html>'
        self.wfile.write(html.encode())

    

    def log_message(self, *args):
        pass

def _find_available_port(start_port=8080, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"No available ports found in range {start_port}-{start_port + max_attempts}")

def _do_oauth2_flow():
    """Execute OAuth2 authorization code flow with PKCE"""
    # Get OAuth2 configuration from API
    oauth_config = _get_oauth_config()
    client_id = oauth_config.get('client_id', CLIENT_ID)
    auth_url = oauth_config.get('auth_url', AUTHENTIK_URL)
    
    # Generate PKCE challenge
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).decode('utf-8').rstrip('=')
    
    # Find available port and start local callback server
    port = _find_available_port()
    OAuth2CallbackHandler.result = None
    server = HTTPServer(('localhost', port), OAuth2CallbackHandler)
    threading.Thread(target=lambda: (server.handle_request(), server.server_close()), daemon=True).start()
    
    # Build and open authorization URL
    auth_endpoint = f"{auth_url}/application/o/authorize/"
    token_endpoint = f"{auth_url}/application/o/token/"
    redirect_uri = f'http://localhost:{port}/callback'
    
    auth_params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': 'openid profile email',
        'state': secrets.token_urlsafe(32),
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
    }
    
    webbrowser.open(f"{auth_endpoint}?{urlencode(auth_params)}")
    
    # Wait for callback (timeout 3 minutes)
    import time
    for _ in range(180):
        if OAuth2CallbackHandler.result:
            break
        time.sleep(1)
    
    result = OAuth2CallbackHandler.result
    if not result or result.get('error'):
        return None
    
    # Exchange code for token
    if result.get('code'):
        return _exchange_code_for_token(result['code'], code_verifier, redirect_uri, token_endpoint, client_id)
    
    return None

def _exchange_code_for_token(code, code_verifier, redirect_uri, token_endpoint, client_id):
    """Exchange authorization code for access token"""
    try:
        r = requests.post(token_endpoint, data={
            'client_id': client_id,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'code_verifier': code_verifier,
        }, timeout=10)
        return r.json() if r.ok else None
    except:
        return None

def get_authenticated_session():
    """Get authenticated session using OAuth2 (browser-based, tokens cached locally)"""
    cache = TokenCache()
    session = requests.Session()
    
    # Try cached token
    token_data = cache.load()
    if token_data and 'access_token' in token_data:
        session.headers['Authorization'] = f"Bearer {token_data['access_token']}"
        try:
            r = session.get(f'{API_BASE_URL}/api/raos', timeout=5, allow_redirects=False)
            if r.status_code == 200:
                return session
        except:
            pass
    
    # Need to authenticate
    token_data = _do_oauth2_flow()
    if token_data and 'access_token' in token_data:
        cache.save(token_data)
        session.headers['Authorization'] = f"Bearer {token_data['access_token']}"
        return session
    
    raise Exception("Authentication failed")
