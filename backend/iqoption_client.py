"""
iqOption SDK Client Wrapper
Provides a simplified interface to the iqOption Broker API

Uses stable_api (IQ_Option) which is more reliable than the basic IQOptionAPI
"""

from iqoptionapi.stable_api import IQ_Option
import logging
from typing import Optional, Dict, Tuple
import time

logger = logging.getLogger(__name__)


class IQOptionClient:
    """Wrapper around iqOption stable_api (IQ_Option) for broker operations"""
    
    def __init__(self, timeout: int = 10):
        """
        Initialize client (not connected yet)
        
        Args:
            timeout: Connection timeout in seconds
        """
        self.timeout = timeout
        self.client: Optional[IQ_Option] = None
        self.is_connected = False
        self.current_mode = "PRACTICE"  # 'PRACTICE' (demo) or 'REAL'
        self.email: Optional[str] = None
    
    def connect(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Authenticate with iqOption Broker using stable_api
        
        Args:
            email: iqOption account email
            password: iqOption account password
        
        Returns:
            Tuple of (success: bool, token: Optional[str])
        """
        try:
            # Initialize IQ_Option client with email and password
            self.client = IQ_Option(email, password)
            self.email = email
            
            logger.info(f"Connecting to iqOption for {email}...")
            
            # Connect to broker - stable_api returns (success, reason)
            connect_result, reason = self.client.connect()
            
            if not connect_result:
                logger.warning(f"Failed to connect to iqOption: {reason}")
                return False, reason or "Connection failed"
            
            # Set to practice (demo) mode by default
            logger.debug(f"Setting account to PRACTICE mode...")
            self.client.change_balance("PRACTICE")
            
            # Get balance to verify connection
            try:
                balance = self.client.get_balance()
                logger.debug(f"Account balance: {balance}")
            except Exception as e:
                logger.warning(f"Could not fetch balance: {str(e)}")
            
            self.is_connected = True
            # Generate a token for session tracking
            token = f"iqoption_{email}_{id(self.client)}"
            logger.info(f"Successfully connected to iqOption for {email}")
            return True, token
                
        except Exception as e:
            logger.error(f"Error connecting to iqOption: {str(e)}")
            self.is_connected = False
            return False, str(e)
    
    def get_balance(self) -> Tuple[bool, Optional[float]]:
        """
        Get current account balance
        
        Returns:
            Tuple of (success: bool, balance: Optional[float])
        """
        try:
            if not self.is_connected or self.client is None:
                return False, None
            
            # Get balance directly from stable_api
            balance = self.client.get_balance()
            logger.debug(f"Balance retrieved: {balance}")
            
            if balance is not None:
                return True, float(balance)
            else:
                logger.warning(f"No balance returned")
                return False, None
                
        except Exception as e:
            logger.error(f"Error getting balance: {str(e)}")
            return False, None
    
    def set_account_type(self, mode: str) -> Tuple[bool, Optional[str]]:
        """
        Switch between demo (PRACTICE) and real (REAL) accounts
        
        Args:
            mode: 'demo', 'practice', 'real', or 'live'
        
        Returns:
            Tuple of (success: bool, message: Optional[str])
        """
        try:
            if not self.is_connected or self.client is None:
                return False, "Not connected"
            
            mode = mode.lower().strip()
            
            # Normalize mode names
            if mode in ['demo', 'practice']:
                sdk_mode = "PRACTICE"
            elif mode in ['real', 'live']:
                sdk_mode = "REAL"
            else:
                return False, f"Invalid mode: {mode}. Use 'demo', 'practice', 'real', or 'live'"
            
            try:
                # Use stable_api change_balance to switch account type
                self.client.change_balance(sdk_mode)
                self.current_mode = sdk_mode
                logger.info(f"Successfully switched to {sdk_mode} account")
                return True, f"Switched to {sdk_mode}"
            except Exception as e:
                logger.error(f"Error switching mode: {str(e)}")
                return False, f"Failed to switch to {sdk_mode}: {str(e)}"
                
        except Exception as e:
            logger.error(f"Error setting account type: {str(e)}")
            return False, str(e)
    
    def disconnect(self) -> bool:
        """Disconnect from iqOption"""
        try:
            if self.client and self.is_connected:
                # IQ_Option doesn't have explicit logout, just close connection
                self.is_connected = False
                self.client = None
                logger.info(f"Disconnected from iqOption for {self.email}")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting: {str(e)}")
            return False


# Global client instance (in production, use proper dependency injection)
_iqoption_client = IQOptionClient()


def get_client() -> IQOptionClient:
    """Get global iqOption client instance"""
    return _iqoption_client
