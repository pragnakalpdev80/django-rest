# api/services.py
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class ExternalAPIService:
    def __init__(self):
        self.base_url = 'https://hp-api.onrender.com'
        # self.api_key = settings.EXTERNAL_API_KEY
    
    def get_data(self, endpoint):
        headers = {
            # 'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'}
        try:
            endpoint = 'api/characters'
            response = requests.get(f'{self.base_url}/{endpoint}', timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            logger.error(f"Timeout calling {endpoint}")
            raise
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error calling {endpoint}: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error calling {endpoint}: {e}")
            raise
    
    def post_data(self, endpoint, data):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        response = requests.post(
            f'{self.base_url}/{endpoint}',
            headers=headers,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        return response.json()