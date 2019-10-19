from deal_with_time import minutes
from vehicle_scheduling.data.load_data import import_trips
from vehicle_scheduling.data.scheduled_trip import ScheduledTrip
from vehicle_scheduling.graph.graph import *


def build_graph(trips: ScheduledTrip):
    graph = Graph()
    nodes = set()
    for trip in trips:
        origin_node = Node(trip.itinerary.origin, minutes(trip.start_time))
        destination_node = Node(trip.itinerary.destination, minutes(trip.end_time))
        arc = Arc(origin_node, destination_node)
        graph.add_arc(arc)
    return graph


if __name__ == '__main__':
    trips = import_trips("/home/eder/py-workspace/transit/vehicle_scheduling/trips_companyT_bussiness_day-07-10-2019")
    network = build_graph(trips)
    network.arcs.sort(key=lambda arc: arc.origin_node.time)
    for arc in network.arcs:
        print(arc)

