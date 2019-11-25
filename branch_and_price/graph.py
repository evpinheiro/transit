from deal_with_time import hour_minute


class Node:
    def __init__(self, code: str, location=None, time=None):
        self.code = code
        self.location = location
        self.time = time

    def __str__(self):
        return str(self.code) if self.location is None or self.time is None else str(self.location) + '-' + str(hour_minute(self.time))


class Arc:
    def __init__(self, origin: Node, destination: Node, upper_bound: int, lower_bound=0):
        self.origin = origin
        self.destination = destination
        self.capacity = upper_bound
        self.lower_bound = lower_bound

    def __str__(self):
        return str(self.origin) + "-" + str(self.destination)


class Graph:
    def __init__(self, commodity_name, nodes: dict, arcs: dict):
        self.commodity_name = commodity_name
        self.arcs_cost_cap = arcs
        self.nodes_demands = nodes
