from django.http import JsonResponse
from django.views import View

from route.env_loader import get_openroute_api_key
from route.infrastructure.geocoding_api import GeocodingAPI
from route.infrastructure.routing_api import RoutingAPI
from route.repositories.fuel_station_repository import FuelStationRepository
from route.domain.strategies import CheapestFuelStrategy
from route.services.route_service import RouteService


def _build_route_service() -> RouteService:
    api_key = get_openroute_api_key()
    geocoding_api = GeocodingAPI(api_key=api_key)
    routing_api = RoutingAPI(api_key=api_key)
    repository = FuelStationRepository()
    strategy = CheapestFuelStrategy()
    return RouteService(
        routing_api=routing_api,
        geocoding_api=geocoding_api,
        strategy=strategy,
        repository=repository,
    )


class RouteAPIView(View):
    """
    GET /api/route/?start=<location>&end=<location>
    Returns route map (coordinates), optimal fuel stops, and total fuel cost.
    API key is read from .env file only (OPENROUTESERVICE_API_KEY).
    """

    def get(self, request):
        start = request.GET.get("start", "").strip()
        end = request.GET.get("end", "").strip()
        if not start or not end:
            return JsonResponse(
                {"error": "Missing required query parameters: start and end"},
                status=400,
            )

        if not get_openroute_api_key():
            return JsonResponse(
                {"error": "OPENROUTESERVICE_API_KEY not set in .env file"},
                status=500,
            )

        service = _build_route_service()
        try:
            result = service.calculate_route(start=start, end=end)
        except Exception as e:
            return JsonResponse(
                {"error": str(e)},
                status=502,
            )

        route = result["route"]
        optimization = result["optimization"]

        payload = {
            "route": {
                "start": route.start,
                "end": route.end,
                "distance_miles": round(route.distance_miles, 2),
                # "coordinates": route.coordinates,
            },
            "fuel_stops": optimization["fuel_stops"],
            "total_fuel_cost_usd": optimization["total_cost"],
            "total_gallons_needed": optimization["total_gallons_needed"],
            "estimated_stops": optimization["estimated_stops"],
            "vehicle_mpg": CheapestFuelStrategy.MPG,
            "vehicle_max_range_miles": CheapestFuelStrategy.MAX_RANGE_MILES,
        }
        return JsonResponse(payload)


