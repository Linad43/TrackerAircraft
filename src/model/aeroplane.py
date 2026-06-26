from src.model.aeroplaneABC import BaseAeroplane


class Aeroplane(BaseAeroplane):
    icao24: str
    callsign: str
    country: str
    velocity: float
    geo_altitude: float

    def __init__(
            self,
            icao24: str,
            callsign: str,
            country: str,
            velocity: float,
            geo_altitude: float
    ) -> None:
        self.icao24 = icao24
        self.callsign = callsign
        self.country = country
        self.velocity = velocity
        self.geo_altitude = geo_altitude

    @classmethod
    def cast_to_object_list(cls, aeroplanes: dict) -> list[Aeroplane]:
        result = []
        for aeroplane in aeroplanes['states']:
            result.append(Aeroplane(
                aeroplane[0],
                aeroplane[1],
                aeroplane[2],
                aeroplane[9],
                aeroplane[13]
            ))
        return result

    def to_dict(self) -> dict:
        return {
            self.icao24: {
                'callsign': self.callsign,
                'country': self.country,
                'velocity': self.velocity,
                'geo_altitude': self.geo_altitude
            }
        }

    def __str__(self):
        return f'{self.icao24}: {self.callsign}, {self.country}, {self.velocity}, {self.geo_altitude}'

    def __repr__(self):
        return f'[{self.icao24}] [{self.callsign}] [{self.country}] [{self.velocity}] [{self.geo_altitude}]'

    def __eq__(self, other):
        return self.velocity == other.velocity and self.geo_altitude == other.geo_altitude
