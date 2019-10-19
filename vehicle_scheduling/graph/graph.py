class Graph:

    def __init__(self):
        self.nodes = set()
        self.arcs = []

    def add_arc(self, arc):
        self.arcs.append(arc)


class Arc:

    def __init__(self, origin_node, destination_node):
        self.origin_node = origin_node
        self.destination_node = destination_node

    def __str__(self):
        return str(self.origin_node) + ' -> ' + str(self.destination_node)


class Node:

    def __init__(self, station, time):
        self.station = station
        self.time = time

    def __str__(self):
        return str(self.station) + '-' + str(self.time)

