from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Route():
    start:str
    end:str
    distance_miles:float
    coordinates:List[Tuple[float, float]]


@dataclass
class FuelStop:
    station_name: str
    city: str
    state: str
    price_per_gallon: float
    gallons_filled: float
    total_cost: float
