from deal_with_time import hour_minute
from enum import Enum


class Node:
    def __init__(self, code: str, location=None, time=None):
        self.code = code
        self.location = location
        self.time = time

    def get_code(self):
        return self.code

    def __str__(self):
        return str(self.code) if self.location is None or self.time is None else str(self.location) + '-' + str(
            hour_minute(self.time))


class ArcType(Enum):
    TRIP = 'trip'
    PULL_IN = 'pull_in'
    PULL_OUT = 'pull_out'
    DEADHEAD_TRIP = 'deadhead_trip'
    CIRCULATION = 'circulation'
    STOPPED = 'stopped'


class Arc:
    def __init__(self, arc_type: ArcType, origin: Node, destination: Node, upper_bound: int, lower_bound=0):
        self.arc_type = arc_type
        self.origin = origin
        self.destination = destination
        self.capacity = upper_bound
        self.lower_bound = lower_bound

    def get_code(self):
        return self.origin.get_code() + "-" + self.destination.get_code()

    def __str__(self):
        return str(self.origin) + "-" + str(self.destination) + '-' + self.arc_type.value


class Graph:
    """
    arcs: dict Arc -> (cost, capacity)
    """
    def __init__(self, commodity_name, nodes: dict, arcs: dict):
        self.commodity_name = commodity_name
        self.arcs_cost_cap = arcs
        self.nodes_demands = nodes

    def get_trip_arcs(self):
        trip_arcs = []
        for arc in self.arcs_cost_cap.items():
            if arc[0].arc_type == ArcType.TRIP:
                trip_arcs.append(arc)
        return trip_arcs
