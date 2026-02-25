# api/services.py
import requests
from django.conf import settings
import logging
from tenacity import retry, stop_after_attempt, wait_exponential


logger = logging.getLogger(__name__)

class ExternalAPIService:
    def __init__(self):
        self.base_url = 'https://hp-api.onrender.com'
        # self.api_key = settings.EXTERNAL_API_KEY
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def get_characters(self):
        try:
            endpoint = 'api/characters'
            response = requests.get(f'{self.base_url}/{endpoint}', timeout=10)
            # response.raise_for_status()
            # print(response.json())
            
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
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def get_hogwarts_staff(self):
        try:
            endpoint = 'api/characters/staff'
            response = requests.get(f'{self.base_url}/{endpoint}', timeout=10)
            response.raise_for_status()
            # print(response.json())
            
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
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    def get_characters_by_house(self,housename):
        try:
            endpoint = 'api/characters/house'
            print(f'{self.base_url}/{endpoint}/{housename}')
            response = requests.get(f'{self.base_url}/{endpoint}/{house}', timeout=10)
            # response.raise_for_status()
            # print(response.json())
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
    
if __name__== "__main__":
    api = ExternalAPIService()
    a=api.get_characters_by_house(housename='gryffindor')
    print(a)