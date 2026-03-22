from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime
from session_manager import SessionManager, require_session
from credential_store import CredentialStore, CredentialValidator
from iqoption_client import get_client as get_iqoption_client
import logging

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize managers
app.session_manager = SessionManager(
    session_timeout_minutes=int(os.getenv('SESSION_TIMEOUT_MINUTES', 30))
)
app.credential_store = CredentialStore()
app.credential_validator = CredentialValidator()

# Track per-session iqOption clients
# Format: {session_id: iqoption_client_instance}
app.session_clients = {}

# ============== Health & Status Endpoints ==============
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'message': 'Backend service is running'})

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify({
        'data': 'Sample data from backend',
        'timestamp': datetime.now().isoformat()
    })

# ============== Broker Authentication Endpoints ==============

@app.route('/api/broker/login', methods=['POST'])
def broker_login():
    """
    Authenticate with iqOption broker using real API
    Request: {email: string, password: string}
    Response: {status: string, sessionId: string, mode: string}
    """
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validate input
        if not email or not password:
            return jsonify({'error': 'Missing email or password'}), 400
        
        if not app.credential_validator.validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not app.credential_validator.validate_password(password):
            return jsonify({'error': 'Password too short (minimum 6 characters)'}), 400
        
        # Create new iqOption client instance for this session
        iqoption_client = get_iqoption_client()
        success, token = iqoption_client.connect(email, password)
        
        if not success:
            logger.warning(f"Failed to authenticate with iqOption: {token}")
            return jsonify({'error': f'Authentication failed: {token or "Unknown error"}'}), 401
        
        # Store encrypted credentials
        app.credential_store.store_credential(email, token)
        
        # Create session
        session_id = app.session_manager.create_session(email, token, mode="practice")
        
        # Store client instance for this session
        app.session_clients[session_id] = iqoption_client
        
        logger.info(f"Successfully authenticated {email} with iqOption")
        
        return jsonify({
            'status': 'authenticated',
            'sessionId': session_id,
            'mode': 'practice',
            'message': f'Successfully authenticated as {email}'
        }), 200
    
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': f'Login failed: {str(e)}'}), 500


@app.route('/api/broker/logout', methods=['POST'])
def broker_logout():
    """
    Logout from iqOption broker and terminate session
    Request: {sessionId: string} (or X-Session-Id header)
    Response: {status: string}
    """
    try:
        data = request.get_json() or {}
        session_id = data.get('sessionId') or request.headers.get('X-Session-Id')
        
        if not session_id:
            return jsonify({'error': 'Missing session ID'}), 401
        
        session = app.session_manager.get_session(session_id)
        # if not session:
        #     return jsonify({'error': 'Invalid or expired session'}), 401
        
        # Disconnect iqOption client if it exists
        if session_id in app.session_clients:
            client = app.session_clients[session_id]
            client.disconnect()
            del app.session_clients[session_id]
            logger.info(f"Disconnected iqOption client for session {session_id}")
        
        # Delete session
        app.session_manager.delete_session(session_id)
        
        return jsonify({
            'status': 'logged_out',
            'message': 'Successfully logged out'
        }), 200
    
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': f'Logout failed: {str(e)}'}), 500


@app.route('/api/broker/balance', methods=['GET'])
def get_broker_balance():
    """
    Get current account balance for authenticated user from real iqOption API
    Query params: sessionId (or X-Session-Id header)
    Response: {balance: float, currency: string, mode: string, lastUpdated: string}
    """
    try:
        session_id = request.args.get('sessionId') or request.headers.get('X-Session-Id')
        
        if not session_id:
            return jsonify({'error': 'Missing session ID'}), 401
        
        session = app.session_manager.get_session(session_id)
        if not session:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        # Get client for this session
        if session_id not in app.session_clients:
            return jsonify({'error': 'iqOption client not initialized for this session'}), 500
        
        client = app.session_clients[session_id]
        mode = session.get('mode', 'demo')
        
        # Fetch real balance from iqOption SDK
        success, balance = client.get_balance()
        
        if not success or balance is None:
            logger.warning(f"Failed to fetch balance for session {session_id}")
            # Return fallback with error indication
            return jsonify({
                'balance': None,
                'error': 'Could not fetch balance from broker',
                'mode': mode,
                'lastUpdated': datetime.utcnow().isoformat()
            }), 503
        
        logger.debug(f"Fetched balance {balance} for session {session_id} (mode: {mode})")
        
        return jsonify({
            'balance': balance,
            'currency': 'USD',
            'mode': mode,
            'lastUpdated': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Balance fetch error: {str(e)}")
        return jsonify({'error': f'Failed to retrieve balance: {str(e)}'}), 500


@app.route('/api/broker/mode/switch', methods=['POST'])
def switch_broker_mode():
    """
    Switch between practice (demo) and real (live) trading modes using iqOption API
    Request: {sessionId: string, mode: string} or X-Session-Id header
    Response: {mode: string, balance: float, message: string}
    """
    try:
        data = request.get_json() or {}
        session_id = data.get('sessionId') or request.headers.get('X-Session-Id')
        new_mode = data.get('mode', '').lower().strip()
        
        # Validate inputs
        if not session_id:
            return jsonify({'error': 'Missing session ID'}), 401
        
        # Accept multiple names for modes
        if new_mode in ['demo', 'practice']:
            user_mode = 'practice'
            sdk_mode = 'PRACTICE'
        elif new_mode in ['live', 'real']:
            user_mode = 'live'
            sdk_mode = 'REAL'
        else:
            return jsonify({'error': 'Invalid mode. Must be "practice", "demo", "live", or "real"'}), 400
        
        session = app.session_manager.get_session(session_id)
        if not session:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        # Get client for this session
        if session_id not in app.session_clients:
            return jsonify({'error': 'iqOption client not initialized for this session'}), 500
        
        client = app.session_clients[session_id]
        
        # Switch account type via iqOption SDK
        success, message = client.set_account_type(sdk_mode)
        
        if not success:
            logger.warning(f"Failed to switch mode for session {session_id}: {message}")
            return jsonify({'error': f'Mode switch failed: {message}'}), 400
        
        # Update mode in session
        app.session_manager.update_mode(session_id, user_mode)
        
        # Fetch balance in new mode
        balance_success, balance = client.get_balance()
        balance = balance if balance_success else None
        
        logger.info(f"Successfully switched session {session_id} to {user_mode} mode")
        
        return jsonify({
            'mode': user_mode,
            'balance': balance,
            'currency': 'USD',
            'message': f'Successfully switched to {user_mode} mode',
            'lastUpdated': datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Mode switch error: {str(e)}")
        return jsonify({'error': f'Mode switch failed: {str(e)}'}), 500


# ============== Trading Endpoints ==============
# Note: These endpoints are for backward compatibility.
# Primary authentication and trading operations should use /api/broker/* endpoints

@app.route('/api/trading/status', methods=['GET'])
def get_trading_status():
    """Get current trading connection status"""
    return jsonify({
        'connected': True,  # Will be connected if using broker endpoints
        'account_type': 'practice',
        'broker': 'iqOption',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/trading/connect', methods=['POST'])
def connect_broker():
    """Connect to broker - deprecated, use /api/broker/login instead"""
    return jsonify({
        'success': False,
        'message': 'Use /api/broker/login for authentication',
        'timestamp': datetime.now().isoformat()
    }), 400

@app.route('/api/trading/disconnect', methods=['POST'])
def disconnect_broker():
    """Disconnect from broker - deprecated, use /api/broker/logout instead"""
    return jsonify({
        'success': False,
        'message': 'Use /api/broker/logout for logout',
        'timestamp': datetime.now().isoformat()
    }), 400

@app.route('/api/trading/account', methods=['GET'])
def get_account_info():
    """Get account information - use /api/broker/balance instead"""
    return jsonify({
        'error': 'Use /api/broker/balance for account information',
        'timestamp': datetime.now().isoformat()
    }), 400

@app.route('/api/trading/account/switch', methods=['POST'])
def switch_account():
    """Switch between demo and real account - use /api/broker/mode/switch instead"""
    return jsonify({
        'error': 'Use /api/broker/mode/switch for mode switching',
        'timestamp': datetime.now().isoformat()
    }), 400

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port)
