class Itinerary:

    def __init__(self, route_name, direction, kind, origin, destination):
        self.route_name = route_name
        self.direction = direction
        self.kind = kind
        self.origin = origin
        self.destination = destination

    def __str__(self) -> str:
        return str(self.route_name) + "-" + str(self.direction) + "-" + str(self.kind) \
               + "-" + str(self.origin) + "-" + str(self.destination)



