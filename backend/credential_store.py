"""
Credential Storage Utility for iqOption Integration
Handles secure encryption/decryption of user credentials and API tokens
"""

import os
import json
from typing import Dict, Optional, Any
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode, urlsafe_b64decode
import hashlib


class CredentialStore:
    """Secure credential storage with encryption"""
    
    def __init__(self):
        """Initialize credential store with encryption key from environment"""
        # Get or generate encryption key
        key_material = os.getenv('CREDENTIAL_ENCRYPTION_KEY')
        
        if not key_material:
            raise ValueError(
                "CREDENTIAL_ENCRYPTION_KEY not set in environment. "
                "Generate with: from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
            )
        
        try:
            self.cipher = Fernet(key_material.encode())
        except Exception as e:
            raise ValueError(f"Invalid encryption key: {str(e)}")
        
        self.credentials_cache = {}  # {email: {encrypted_token, broker_config}}
    
    def store_credential(self, email: str, iqoption_token: str, 
                        broker_config: Optional[Dict[str, Any]] = None) -> bool:
        """
        Store encrypted iqOption token for a user
        
        Args:
            email: User email address
            iqoption_token: iqOption authentication token
            broker_config: Optional broker configuration
            
        Returns:
            True if stored successfully
        """
        try:
            # Encrypt the token
            encrypted_token = self.cipher.encrypt(iqoption_token.encode()).decode()
            
            # Store in cache (in production, use database)
            self.credentials_cache[email] = {
                "encrypted_token": encrypted_token,
                "broker_config": broker_config or {},
                "stored_at": self._get_timestamp()
            }
            
            return True
        except Exception as e:
            print(f"Error storing credential for {email}: {str(e)}")
            return False
    
    def retrieve_credential(self, email: str) -> Optional[str]:
        """
        Retrieve and decrypt iqOption token for a user
        
        Args:
            email: User email address
            
        Returns:
            Decrypted token or None if not found
        """
        try:
            if email not in self.credentials_cache:
                return None
            
            encrypted_token = self.credentials_cache[email]["encrypted_token"]
            decrypted_token = self.cipher.decrypt(encrypted_token.encode()).decode()
            
            return decrypted_token
        except Exception as e:
            print(f"Error retrieving credential for {email}: {str(e)}")
            return None
    
    def delete_credential(self, email: str) -> bool:
        """
        Delete stored credentials for a user
        
        Args:
            email: User email address
            
        Returns:
            True if deleted, False if not found
        """
        if email in self.credentials_cache:
            del self.credentials_cache[email]
            return True
        return False
    
    def get_broker_config(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve broker configuration for a user
        
        Args:
            email: User email address
            
        Returns:
            Broker config dict or None if not found
        """
        if email in self.credentials_cache:
            return self.credentials_cache[email].get("broker_config")
        return None
    
    @staticmethod
    def hash_token(token: str) -> str:
        """
        Create secure hash of token for logging/audit purposes
        
        Args:
            token: Token to hash
            
        Returns:
            SHA256 hash (first 8 chars for display)
        """
        hash_obj = hashlib.sha256(token.encode())
        return hash_obj.hexdigest()[:8]
    
    @staticmethod
    def _get_timestamp() -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat()


class CredentialValidator:
    """Validate user credentials before storing"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email to validate
            
        Returns:
            True if valid format
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_password(password: str, min_length: int = 6) -> bool:
        """
        Validate password strength
        
        Args:
            password: Password to validate
            min_length: Minimum password length
            
        Returns:
            True if meets requirements
        """
        if len(password) < min_length:
            return False
        return True
    
    @staticmethod
    def validate_token(token: str) -> bool:
        """
        Validate iqOption token format
        
        Args:
            token: Token to validate
            
        Returns:
            True if appears valid
        """
        # Basic validation - token should be non-empty string
        return isinstance(token, str) and len(token) > 0
