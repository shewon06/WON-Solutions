import requests
import hashlib
import hmac
import time
import json
from datetime import datetime, timedelta

class DarazClient:
    BASE_URL = "https://api.daraz.lk/rest" # Default for Sri Lanka

    def __init__(self, app_key, app_secret, access_token=None):
        self.app_key = app_key
        self.app_secret = app_secret
        self.access_token = access_token

    def _generate_signature(self, api_name, params):
        # 1. Sort parameters by name
        sorted_params = sorted(params.items())
        
        # 2. Concatenate parameters
        param_str = "".join(f"{k}{v}" for k, v in sorted_params)
        
        # 3. Build the string to sign: api_name + sorted_params
        sign_base = api_name + param_str
        
        # 4. HMAC-SHA256 signature
        signature = hmac.new(
            self.app_secret.encode('utf-8'),
            sign_base.encode('utf-8'),
            hashlib.sha256
        ).hexdigest().upper()
        
        return signature

    def call_api(self, api_name, params=None, method='GET'):
        if params is None:
            params = {}

        # Common parameters
        common_params = {
            'app_key': self.app_key,
            'timestamp': str(int(time.time() * 1000)),
            'sign_method': 'sha256',
        }
        
        if self.access_token:
            common_params['access_token'] = self.access_token

        # Merge params
        all_params = {**common_params, **params}
        
        # Generate signature
        all_params['sign'] = self._generate_signature(api_name, all_params)

        try:
            if method.upper() == 'GET':
                response = requests.get(self.BASE_URL + api_name, params=all_params)
            else:
                response = requests.post(self.BASE_URL + api_name, params=all_params)
            
            return response.json()
        except Exception as e:
            return {'code': 'Error', 'message': str(e)}

    def get_products(self, offset=0, limit=20):
        params = {
            'offset': str(offset),
            'limit': str(limit)
        }
        return self.call_api('/products/get', params)

    def exchange_code_for_token(self, code):
        # This is usually a POSI to /auth/token/create
        # Base URL might be different for Auth
        AUTH_URL = "https://auth.daraz.com/rest/auth/token/create"
        params = {
            'app_key': self.app_key,
            'timestamp': str(int(time.time() * 1000)),
            'sign_method': 'sha256',
            'code': code
        }
        params['sign'] = self._generate_signature('/auth/token/create', params)
        
        try:
            response = requests.get(AUTH_URL, params=params)
            return response.json()
        except Exception as e:
            return {'code': 'Error', 'message': str(e)}
