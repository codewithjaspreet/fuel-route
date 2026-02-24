import math
from typing import Dict, List, Any
from route.domain.entities import Route
from route.domain.interfaces import FuelOptimizationStrategy


class CheapestFuelStrategy(FuelOptimizationStrategy):
    """
    Simple approach: need N stops (every 500 mi), pick the N cheapest stations
    in the DB and assign one per stop. Cost-effective, no geography logic.
    """
    MAX_RANGE_MILES = 500
    MPG = 10

    def find_fuel_stops(self, route: Route, stations: List) -> Dict[str, Any]:
        total_distance = route.distance_miles
        total_gallons_needed = total_distance / self.MPG
        num_stops = max(1, math.ceil(total_distance / self.MAX_RANGE_MILES))

        sorted_stations = sorted(stations, key=lambda s: s.retail_price)[:num_stops]
        gallons_per_full_stop = self.MAX_RANGE_MILES / self.MPG  # 50 gal

        fuel_stops: List[Dict[str, Any]] = []
        total_cost = 0.0

        for i, station in enumerate(sorted_stations):
            if i == num_stops - 1:
                miles_left = total_distance - (i * self.MAX_RANGE_MILES)
                gallons_this_stop = miles_left / self.MPG
            else:
                gallons_this_stop = gallons_per_full_stop

            stop_cost = round(gallons_this_stop * station.retail_price, 2)
            total_cost += stop_cost
            fuel_stops.append({
                "station_name": station.name,
                "address": station.address,
                "city": station.city,
                "state": station.state,
                "price_per_gallon": round(station.retail_price, 2),
                "gallons_filled": round(gallons_this_stop, 2),
                "total_cost": stop_cost,
            })

        return {
            "fuel_stops": fuel_stops,
            "total_cost": round(total_cost, 2),
            "estimated_stops": num_stops,
            "total_gallons_needed": round(total_gallons_needed, 2),
        }