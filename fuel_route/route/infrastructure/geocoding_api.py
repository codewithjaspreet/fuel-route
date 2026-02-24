import requests
from django.conf import settings
from django.core.cache import cache


class GeocodingAPI:

    BASE_URL = "https://api.openrouteservice.org/geocode/search"
    CACHE_KEY_PREFIX = "geocode:"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _cache_key(self, location: str) -> str:
        normalized = " ".join(location.strip().lower().split())
        return f"{self.CACHE_KEY_PREFIX}{normalized}"

    def get_coordinates(self, location: str) -> tuple:
        cache_key = self._cache_key(location)
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        params = {
            "api_key": self.api_key,
            "text": location,
            "size": 1
        }

        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected API response type: {type(data).__name__}")

        features = data.get("features")
        if not features or not isinstance(features, list):
            err = data.get("error") or data.get("message") or data
            raise ValueError(f"Geocoding API returned no result: {err}")

        coordinates = features[0]["geometry"]["coordinates"]
        result = (coordinates[1], coordinates[0])

        timeout = getattr(
            settings,
            "GEOCODE_CACHE_TIMEOUT_SECONDS",
            7 * 24 * 60 * 60
        )
        cache.set(cache_key, result, timeout=timeout)

        return result