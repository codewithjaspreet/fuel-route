from abc import ABC, abstractmethod
from typing import Dict, List
from route.domain.entities import Route


class FuelOptimizationStrategy(ABC):

    @abstractmethod
    def find_fuel_stops(self, route: Route, stations: List) -> Dict:
        """
        Should return:
        {
            "fuel_stops": [...],
            "total_cost": float
        }
        """
        pass