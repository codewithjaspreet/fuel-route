from typing import List
from route.models import FuelStation


class FuelStationRepository:

    def get_all_stations(self) -> List[FuelStation]:
        return list(FuelStation.objects.all())

    def get_stations_by_state(self,state:str) -> List[FuelStation]:
        return FuelStation.objects.filter(state=state)

