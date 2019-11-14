from deal_with_time import hour_minute
from vehicle_scheduling.data_model.scheduled_event import ScheduledEvent


class Arc:

    def __init__(self, origin_node, destination_node, cost: int, capacity: int, scheduling_event: ScheduledEvent):
        self.scheduling_event = scheduling_event
        self.origin_node = origin_node
        self.destination_node = destination_node
        self.cost = cost
        self.capacity = capacity

    def __str__(self):
        return str(self.origin_node) + ' -> ' + str(self.destination_node) + ': ' + str(self.scheduling_event)


class Node:

    def __init__(self, station: str, time: int, demand: int, position_station_representation: int):
        self.station = station
        self.time = time
        self.demand = demand
        self.position_station_representation = position_station_representation

    def __str__(self):
        return str(self.station) + '-' + str(hour_minute(self.time))

    def __eq__(self, other):
        self.station == other.station
        self.time == other.time

    def __hash__(self):
        return self.__str__().__hash__()


class Graph:

    def __init__(self, commodity: str):
        self.commodity = commodity
        self.nodes = set([])
        self.all_arcs = []
        self.trip_arcs = []

    def add_arc(self, arc: Arc):
        self.all_arcs.append(arc)
        self.nodes.add(arc.origin_node)
        self.nodes.add(arc.destination_node)


if __name__ == '__main__':
    graph = Graph('D1')
    node1 = Node("s1", 480)
    node2 = Node("s1", 540)
    node3 = Node("s2", 495)
    node4 = Node("s2", 525)
    graph.add_arc(Arc(node1, node4, 0, None))
    graph.add_arc(Arc(node3, node2, 0, None))
    graph.add_arc(Arc(node1, node2, 0, None))
    print([node.__str__() for node in graph.nodes])
