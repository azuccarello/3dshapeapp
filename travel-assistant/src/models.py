"""Core data types describing a parsed travel itinerary."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class StopType(Enum):
    ORIGIN = "origin"
    LAYOVER = "layover"
    FINAL_DESTINATION = "final_destination"


@dataclass
class FlightLeg:
    flight_number: str
    airline: str
    origin: str  # IATA code
    destination: str  # IATA code
    departure_time: datetime
    arrival_time: datetime
    confirmation_number: str | None = None


@dataclass
class Stop:
    airport: str  # IATA code
    arrival_time: datetime | None
    departure_time: datetime | None
    stop_type: StopType


@dataclass
class Itinerary:
    trip_name: str
    legs: list[FlightLeg] = field(default_factory=list)
    source_email_ids: list[str] = field(default_factory=list)

    @property
    def stops(self) -> list[Stop]:
        """Derive the ordered stops (origin, layovers, final destination) from the flight legs."""
        if not self.legs:
            return []

        stops: list[Stop] = []
        first_leg = self.legs[0]
        stops.append(Stop(
            airport=first_leg.origin,
            arrival_time=None,
            departure_time=first_leg.departure_time,
            stop_type=StopType.ORIGIN,
        ))

        for i, leg in enumerate(self.legs):
            is_last = i == len(self.legs) - 1
            next_departure = None if is_last else self.legs[i + 1].departure_time
            stop_type = StopType.FINAL_DESTINATION if is_last else StopType.LAYOVER
            stops.append(Stop(
                airport=leg.destination,
                arrival_time=leg.arrival_time,
                departure_time=next_departure,
                stop_type=stop_type,
            ))

        return stops
