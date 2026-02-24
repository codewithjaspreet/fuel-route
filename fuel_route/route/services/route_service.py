from route.domain.entities import Route
from route.domain.interfaces import FuelOptimizationStrategy
from route.infrastructure.routing_api import RoutingAPI
from route.infrastructure.geocoding_api import GeocodingAPI
from route.repositories.fuel_station_repository import FuelStationRepository


class RouteService:

    def __init__(
        self,
        routing_api: RoutingAPI,
        geocoding_api: GeocodingAPI,
        strategy: FuelOptimizationStrategy,
        repository: FuelStationRepository
    ):
        self.routing_api = routing_api
        self.geocoding_api = geocoding_api
        self.strategy = strategy
        self.repository = repository

    def calculate_route(self, start: str, end: str) -> dict:

        start_coords = self.geocoding_api.get_coordinates(start)
        end_coords = self.geocoding_api.get_coordinates(end)

        route_data = self.routing_api.get_route(start_coords, end_coords)

        route = Route(
            start=start,
            end=end,
            distance_miles=route_data["distance_miles"],
            coordinates=route_data["coordinates"]
        )

        stations = self.repository.get_all_stations()

        optimization_result = self.strategy.find_fuel_stops(route, stations)

        return {
            "route": route,
            "optimization": optimization_result
        }