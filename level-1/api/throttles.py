# api/throttles.py
from django.core.cache import caches
from rest_framework.throttling import AnonRateThrottle

class CustomAnonRateThrottle(AnonRateThrottle):
    cache = caches['alternate']  # Use alternate cache backend