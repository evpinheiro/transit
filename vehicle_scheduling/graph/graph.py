from deal_with_time import hour_minute
from vehicle_scheduling.data_model.scheduled_event import ScheduledEvent


class Arc:

    def __init__(self, origin_node, destination_node, scheduling_event: ScheduledEvent, cost: int):
        self.scheduling_event = scheduling_event
        self.origin_node = origin_node
        self.destination_node = destination_node
        self.cost = cost

    def __str__(self):
        return str(self.origin_node) + ' -> ' + str(self.destination_node) + ': ' + str(self.scheduling_event)


class Node:

    def __init__(self, station, time):
        self.station = station
        self.time = time

    def __str__(self):
        return str(self.station) + '-' + str(hour_minute(self.time))


class Graph:

    def __init__(self, commodity: str):
        self.commodity = commodity
        self.nodes = set()
        self.arcs = []

    """
    
    """
    def add_arc(self, arc: Arc):
        self.arcs.append(arc)
        self.nodes.add(arc.origin_node)
        self.nodes.add(arc.destination_node)


if __name__ == '__main__':
    graph = Graph()
    node1 = Node("s1", 480)
    node2 = Node("s1", 540)
    node3 = Node("s2", 495)
    node4 = Node("s2", 525)
    graph.add_arc(Arc(node1, node4, None))
    graph.add_arc(Arc(node3, node2, None))
    graph.add_arc(Arc(node1, node2, None))
    print([node.__str__() for node in graph.nodes])
