from deal_with_time import minutes
from vehicle_scheduling.graph.graph import *
from vehicle_scheduling.data_model.compatible_trips_rules import *


def build_graph(garage_technology: str, _trips: ScheduledTrip, _compatibility_rules: CompatibilityRules):
    _graph = Graph(garage_technology)
    add_trip_arcs(_trips, _graph)
    add_connection_arcs(_trips, _compatibility_rules, _graph)
    return _graph


def add_trip_arcs(_trips: ScheduledTrip, _graph: Graph):
    for trip in _trips:
        origin_node = Node(trip.itinerary.origin, trip.start_time)
        destination_node = Node(trip.itinerary.destination, trip.end_time)
        edge = Arc(origin_node, destination_node, trip, 0)
        _graph.add_arc(edge)


def add_connection_arcs(_trips, _compatibility_rules, _graph: Graph):
    for i, trip_i in enumerate(_trips):
        for j, trip_j in enumerate(_trips):
            if i != j:
                event_between = _compatibility_rules.event_between(trip_i, trip_j)
                if event_between is not None:
                    origin_node = Node(trip_i.itinerary.destination, event_between.start_time)
                    destination_node = Node(trip_j.itinerary.origin, event_between.end_time)
                    edge = Arc(origin_node, destination_node, event_between, event_between.end_time - event_between.start_time)
                    _graph.add_arc(edge)


if __name__ == '__main__':
    # trips = import_trips("/home/eder/py-workspace/transit/vehicle_scheduling/trips_companyT_bussiness_day-07-10-2019")

    # transport network
    deadhead_TISAN_TICAN = Deadhead("TISAN", "TICAN", 15, minutes("00:10"))
    deadhead_TICAN_TISAN = Deadhead("TICAN", "TISAN", 15, minutes("00:10"))
    itinerary_TICEN_TISAN_322 = Itinerary("332", "forward", "normal", "TICEN", "TISAN")
    itinerary_TISAN_TICEN_322 = Itinerary("332", "backward", "normal", "TISAN", "TICEN")
    itinerary_TICEN_TICAN_221 = Itinerary("221", "forward", "normal", "TICEN", "TICAN")
    itinerary_TICAN_TICEN_221 = Itinerary("221", "backward", "normal", "TICAN", "TICEN")

    # compatibility rules
    possible_line_connections = PossibleLineConnections()
    possible_line_connections.add_possible_connection("332", "221")
    possible_deadheads = PossibleDeadheads()
    possible_deadheads.add_possible_deadhead(deadhead_TISAN_TICAN)
    possible_deadheads.add_possible_deadhead(deadhead_TICAN_TISAN)
    min_layover_duration = LayoverTime()
    min_layover_duration.add_layover_time(itinerary_TICEN_TISAN_322, 5)
    min_layover_duration.add_layover_time(itinerary_TISAN_TICEN_322, 3)
    min_layover_duration.add_layover_time(itinerary_TICEN_TICAN_221, 5)
    min_layover_duration.add_layover_time(itinerary_TICAN_TICEN_221, 3)
    compatibility_rules = CompatibilityRules(possible_deadheads, min_layover_duration, possible_line_connections)

    # scheduled trips
    trips1 = ScheduledTrip(minutes("08:00"), minutes("08:50"), itinerary_TICEN_TISAN_322)
    trips2 = ScheduledTrip(minutes("09:00"), minutes("10:55"), itinerary_TISAN_TICEN_322)
    trips3 = ScheduledTrip(minutes("11:00"), minutes("12:20"), itinerary_TICEN_TICAN_221)
    trips4 = ScheduledTrip(minutes("09:00"), minutes("10:20"), itinerary_TICAN_TICEN_221)
    trips = [trips1, trips2, trips3, trips4]
    network = build_graph('garage1-common_vehicle', trips, compatibility_rules)
    # network.arcs.sort(key=lambda _arc: _arc.origin_node.time)
    for arc in network.arcs:
        print(arc)
