import requests


class RoutingAPI:

    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def get_route(self, start_coords: tuple, end_coords: tuple) -> dict:
        # API expects start/end as "lon,lat" strings (coords are (lat, lon))
        start = f"{start_coords[1]},{start_coords[0]}"
        end = f"{end_coords[1]},{end_coords[0]}"
        params = {
            "api_key": self.api_key,
            "start": start,
            "end": end,
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()

        data = response.json()
        if not isinstance(data, dict):
            raise ValueError(f"Unexpected API response type: {type(data).__name__}")

        # GET returns GeoJSON FeatureCollection; POST returns {"routes": [...]}
        routes = data.get("routes")
        features = data.get("features")

        if routes and isinstance(routes, list):
            # POST-style response
            route = routes[0]
            distance_meters = route["summary"]["distance"]
            coordinates = route["geometry"]["coordinates"]
        elif features and isinstance(features, list):
            # GET-style response (GeoJSON FeatureCollection)
            feature = features[0]
            distance_meters = feature["properties"]["summary"]["distance"]
            coordinates = feature["geometry"]["coordinates"]
        else:
            err = data.get("error") or data.get("message") or "No routes or features in response"
            raise ValueError(f"Routing API returned no route: {err}")

        distance_miles = distance_meters / 1609.34
        # API uses [lon, lat]; we store (lat, lon)
        lat_lon_coordinates = [(coord[1], coord[0]) for coord in coordinates]

        return {
            "distance_miles": distance_miles,
            "coordinates": lat_lon_coordinates
        }