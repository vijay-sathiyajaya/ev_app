from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Trading state (dummy data)
trading_state = {
    'connected': False,
    'account_type': 'demo',
    'broker': None,
    'demo_balance': 10000.00,
    'real_balance': 50000.00
}

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

# ============== Trading Endpoints ==============
@app.route('/api/trading/status', methods=['GET'])
def get_trading_status():
    """Get current trading connection status"""
    return jsonify({
        'connected': trading_state['connected'],
        'account_type': trading_state['account_type'],
        'broker': trading_state['broker'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/trading/connect', methods=['POST'])
def connect_broker():
    """Connect to broker"""
    data = request.get_json()
    broker_name = data.get('broker', 'Demo Broker')
    
    trading_state['connected'] = True
    trading_state['broker'] = broker_name
    
    return jsonify({
        'success': True,
        'message': f'Connected to {broker_name}',
        'connected': trading_state['connected'],
        'broker': trading_state['broker'],
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/trading/disconnect', methods=['POST'])
def disconnect_broker():
    """Disconnect from broker"""
    trading_state['connected'] = False
    trading_state['broker'] = None
    
    return jsonify({
        'success': True,
        'message': 'Disconnected from broker',
        'connected': trading_state['connected'],
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/trading/account', methods=['GET'])
def get_account_info():
    """Get account information including balance"""
    account_type = request.args.get('type', trading_state['account_type'])
    balance = trading_state['demo_balance'] if account_type == 'demo' else trading_state['real_balance']
    
    return jsonify({
        'account_type': account_type,
        'balance': balance,
        'currency': 'USD',
        'connected': trading_state['connected'],
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/trading/account/switch', methods=['POST'])
def switch_account():
    """Switch between demo and real account"""
    data = request.get_json()
    new_account_type = data.get('account_type', 'demo')
    
    if new_account_type not in ['demo', 'real']:
        return jsonify({
            'success': False,
            'message': 'Invalid account type. Use "demo" or "real"'
        }), 400
    
    trading_state['account_type'] = new_account_type
    balance = trading_state['demo_balance'] if new_account_type == 'demo' else trading_state['real_balance']
    
    return jsonify({
        'success': True,
        'message': f'Switched to {new_account_type} account',
        'account_type': new_account_type,
        'balance': balance,
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port)
