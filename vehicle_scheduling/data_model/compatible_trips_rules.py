from vehicle_scheduling.data_model.transport_network import *
from vehicle_scheduling.data_model.scheduled_event import *


class PossibleLineConnections:

    def __init__(self):
        self.cache_connections = {}

    def add_possible_connection(self, route_name1: str, route_name2: str):
        if not self.is_possible_connection(route_name1, route_name2):
            self.cache_connections[route_name1] = route_name2

    def is_possible_connection(self, route_name1: str, route_name2: str):
        return route_name1 == route_name2 or self.cache_connections.get(route_name1) == route_name2 \
               or self.cache_connections.get(route_name2) == route_name1


class LayoverTime:

    def __init__(self):
        self.cache_layover = {}

    def add_layover_time(self, itinerary: Itinerary, time_duration: int):
        self.cache_layover[itinerary] = time_duration

    def get_layover_time(self, itinerary: Itinerary):
        return self.cache_layover.get(itinerary, 0)  # return zero with there is no layover


class PossibleDeadheads:

    def __init__(self):
        self.cache_deadheads = {}

    def add_possible_deadhead(self, deadhead: Deadhead):
        key = self.get_key(deadhead.origin, deadhead.destination)
        if self.cache_deadheads.get(key) is None:
            self.cache_deadheads[key] = deadhead

    def get_key(self, origin, destination):
        return origin + "-/" + destination

    def get_deadhead(self, origin, destination) -> Deadhead:
        return self.cache_deadheads.get(self.get_key(origin, destination))


class CompatibilityRules:

    def __init__(self, possible_deadheads: PossibleDeadheads, layover_times: LayoverTime,
                 possible_line_connections: PossibleLineConnections):
        self.possible_deadheads = possible_deadheads
        self.layover_times = layover_times
        self.possible_line_connections = possible_line_connections

    def event_between(self, trip1: ScheduledTrip, trip2: ScheduledTrip) -> ScheduledEvent:
        if not self.possible_line_connections.is_possible_connection(trip1.itinerary.route_name, trip2.itinerary.route_name):
            return None
        min_layover_duration = self.layover_times.get_layover_time(trip2.itinerary)
        if trip2.start_time - trip1.end_time < min_layover_duration:
            return None
        trip1_destination = trip1.itinerary.destination
        trip2_origin = trip2.itinerary.origin
        if trip1_destination == trip2_origin:
            return ScheduledIdleTime(trip1.end_time, trip2.start_time)
        deadhead = self.possible_deadheads.get_deadhead(trip1_destination, trip2_origin)
        if deadhead is None or trip2.start_time - trip1.end_time > deadhead.duration + min_layover_duration:
            return None
        # TODO resolver essa questão que não está certa aqui
        return ScheduledDeadheadTrip(deadhead, trip1.end_time, trip1.end_time + deadhead.duration)


if __name__ == '__main__':
    line_conn = PossibleLineConnections()
    line_conn.add_possible_connection("332", "233")
    print(line_conn.is_possible_connection("233", "332"), "should be true")
    line_conn.add_possible_connection("233", "332")
    print(len(line_conn.cache_connections))
    layover = LayoverTime()
    itinerary1 = Itinerary("332", "ida", "normal", "TICEN", "TISAN")
    layover.add_layover_time(itinerary1, 10)
    print(layover.get_layover_time(itinerary1))
    itinerary2 = Itinerary("332", "ida", "circular", "TICEN", "TISAN")
    print(layover.get_layover_time(itinerary2))
    layover = LayoverTime()
    layover.add_layover_time(itinerary1, 15)
    print(layover.get_layover_time(itinerary1))
