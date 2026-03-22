"""
IQOption Client - HTTP REST API Version
Uses HTTP REST endpoints instead of WebSocket connection
This solves the 404 WebSocket error issue
"""

import requests
import logging
from typing import Optional, Dict, Tuple

logger = logging.getLogger(__name__)


class IQOptionHTTPClient:
    """HTTP REST API based client for IQOption - works around WebSocket 404 issue"""
    
    def __init__(self, timeout: int = 10):
        """Initialize HTTP client"""
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.is_connected = False
        self.ssid = None
        self.user_id = None
        self.email = None
        self.base_url = "https://api.iqoption.com"
    
    def connect(self, email: str, password: str) -> Tuple[bool, Optional[str]]:
        """
        Authenticate using HTTP REST API
        
        Returns:
            Tuple of (success: bool, token: Optional[str])
        """
        try:
            self.email = email
            
            # Use HTTP REST login endpoint instead of WebSocket
            login_url = f"{self.base_url}/v1/login"
            login_data = {
                "email": email,
                "password": password
            }
            
            logger.info(f"Connecting to IQOption via HTTP REST API...")
            response = self.session.post(login_url, json=login_data, timeout=self.timeout)
            
            if response.status_code != 200:
                logger.warning(f"HTTP login failed: {response.status_code}")
                return False, f"HTTP {response.status_code}: {response.text[:100]}"
            
            result = response.json()
            
            # Extract SSID token
            self.ssid = result.get('data', {}).get('ssid')
            
            # For loginv2, extract additional info
            if 'ssid' in result:
                self.ssid = result['ssid']
                self.user_id = result.get('user_id')
            
            if not self.ssid:
                logger.warning("No SSID token in response")
                return False, "No session token received"
            
            self.is_connected = True
            token = f"http_rest_{email}_{self.ssid}"
            logger.info(f"Successfully connected to IQOption via HTTP for {email}")
            logger.debug(f"SSID: {self.ssid}, User ID: {self.user_id}")
            
            return True, token
            
        except Exception as e:
            logger.error(f"Error connecting to IQOption: {str(e)}")
            self.is_connected = False
            return False, str(e)
    
    def get_balance(self) -> Tuple[bool, Optional[float]]:
        """
        Get current account balance via HTTP REST API
        
        Returns:
            Tuple of (success: bool, balance: Optional[float])
        """
        try:
            if not self.is_connected or not self.ssid:
                return False, None
            
            # Add SSID to cookie for authentication
            self.session.cookies.set('ssid', self.ssid)
            
            # Try to get balance using available endpoints
            balance_endpoints = [
                f"{self.base_url}/api/v1/user/balance",
                f"{self.base_url}/v1/user/balance",
                f"{self.base_url}/api/user/profile",  # Profile may contain balance
                f"{self.base_url}/v1/user/profile",
            ]
            
            for endpoint in balance_endpoints:
                try:
                    logger.debug(f"Trying balance endpoint: {endpoint}")
                    response = self.session.get(endpoint, timeout=self.timeout)
                    
                    if response.status_code == 200:
                        data = response.json()
                        logger.debug(f"Balance response: {data}")
                        
                        # Extract balance from response
                        balance = None
                        if isinstance(data, dict):
                            # Look for common balance keys
                            balance = data.get('balance') or data.get('amount')
                            if not balance and 'data' in data:
                                balance = data['data'].get('balance') or data['data'].get('amount')
                        
                        if balance is not None:
                            return True, float(balance)
                            
                except Exception as e:
                    logger.debug(f"Endpoint {endpoint} failed: {str(e)}")
                    continue
            
            logger.warning("No balance endpoint returned valid data")
            return False, None
            
        except Exception as e:
            logger.error(f"Error getting balance: {str(e)}")
            return False, None
    
    def get_profile(self) -> Tuple[bool, Optional[Dict]]:
        """
        Get user profile information
        
        Returns:
            Tuple of (success: bool, profile_data: Optional[Dict])
        """
        try:
            if not self.is_connected or not self.ssid:
                return False, None
            
            self.session.cookies.set('ssid', self.ssid)
            
            profile_endpoints = [
                f"{self.base_url}/v1/user/profile",
                f"{self.base_url}/api/v1/user/profile",
            ]
            
            for endpoint in profile_endpoints:
                try:
                    response = self.session.get(endpoint, timeout=self.timeout)
                    if response.status_code == 200:
                        return True, response.json()
                except:
                    continue
            
            return False, None
            
        except Exception as e:
            logger.error(f"Error getting profile: {str(e)}")
            return False, None
    
    def disconnect(self) -> bool:
        """Disconnect and clean up"""
        try:
            self.is_connected = False
            self.ssid = None
            self.session.close()
            logger.info(f"Disconnected from IQOption")
            return True
        except Exception as e:
            logger.error(f"Error disconnecting: {str(e)}")
            return False


# For testing
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.DEBUG)
    
    client = IQOptionHTTPClient()
    
    email = "your_email@example.com"
    password = "your_password"
    
    # Connect
    success, token = client.connect(email, password)
    print(f"Connect: {success}, Token: {token}")
    
    if success:
        # Get balance
        success, balance = client.get_balance()
        print(f"Balance: {balance}")
        
        # Get profile
        success, profile = client.get_profile()
        print(f"Profile: {profile}")
        
        # Disconnect
        client.disconnect()
