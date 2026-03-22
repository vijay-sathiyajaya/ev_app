"""
Session Management Module for iqOption Broker Integration
Handles authentication tokens, session persistence, and credential management
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from functools import wraps
from flask import request, jsonify


class SessionManager:
    """Manages broker sessions and authentication tokens"""
    
    def __init__(self, session_timeout_minutes: int = 30):
        """
        Initialize session manager
        
        Args:
            session_timeout_minutes: Duration before session expires
        """
        self.sessions = {}  # {session_id: {user_data, token, expiration, mode}}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
    
    def create_session(self, email: str, iqoption_token: str, mode: str = "demo") -> str:
        """
        Create a new session for an authenticated user
        
        Args:
            email: User email address
            iqoption_token: Authentication token from iqOption broker
            mode: Trading mode (demo or live)
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        expiration = datetime.utcnow() + self.session_timeout
        
        self.sessions[session_id] = {
            "email": email,
            "iqoption_token": iqoption_token,
            "mode": mode,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expiration.isoformat(),
            "last_activity": datetime.utcnow().isoformat()
        }
        
        return session_id
    
    def validate_session(self, session_id: str) -> bool:
        """
        Validate if a session exists and is not expired
        
        Args:
            session_id: The session ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        expiration = datetime.fromisoformat(session["expires_at"])
        
        if datetime.utcnow() > expiration:
            del self.sessions[session_id]
            return False
        
        # Update last activity
        session["last_activity"] = datetime.utcnow().isoformat()
        return True
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session data if valid
        
        Args:
            session_id: The session ID to retrieve
            
        Returns:
            Session data dict or None if invalid/expired
        """
        if self.validate_session(session_id):
            return self.sessions[session_id]
        return None
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a session (e.g., on logout)
        
        Args:
            session_id: The session ID to delete
            
        Returns:
            True if deleted, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def update_mode(self, session_id: str, new_mode: str) -> bool:
        """
        Update trading mode for a session
        
        Args:
            session_id: The session ID
            new_mode: New mode (demo or live)
            
        Returns:
            True if updated, False if session invalid
        """
        session = self.get_session(session_id)
        if session:
            session["mode"] = new_mode
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove all expired sessions
        
        Returns:
            Number of sessions cleaned up
        """
        expired = []
        for session_id, session in self.sessions.items():
            expiration = datetime.fromisoformat(session["expires_at"])
            if datetime.utcnow() > expiration:
                expired.append(session_id)
        
        for session_id in expired:
            del self.sessions[session_id]
        
        return len(expired)


def require_session(f):
    """
    Decorator to require valid session for API endpoint
    
    Extracts sessionId from request and validates it.
    Passes session data to the route handler.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        session_id = request.headers.get('X-Session-Id') or request.args.get('sessionId')
        
        if not session_id:
            return jsonify({'error': 'Missing session ID'}), 401
        
        # Access global session manager (will be injected)
        from flask import current_app
        if not hasattr(current_app, 'session_manager'):
            return jsonify({'error': 'Session manager not initialized'}), 500
        
        session = current_app.session_manager.get_session(session_id)
        if not session:
            return jsonify({'error': 'Invalid or expired session'}), 401
        
        # Pass session to route handler
        return f(session=session, session_id=session_id, *args, **kwargs)
    
    return decorated_function
