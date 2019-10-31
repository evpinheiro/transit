from deal_with_time import minutes
from vehicle_scheduling.graph.graph import *
from vehicle_scheduling.data_model.compatible_trips_rules import *


def build_graph(garage_technology: str, garage_tec_capacity: int, _trips: ScheduledTrip,
                _compatibility_rules: CompatibilityRules):
    _graph = Graph(garage_technology)
    trip_arcs = []
    add_trip_arcs(garage_tec_capacity, _trips, trip_arcs, _graph)
    add_connection_arcs(garage_tec_capacity, trip_arcs, _compatibility_rules, _graph)
    return _graph


def add_trip_arcs(garage_tec_capacity: int, _trips: ScheduledTrip, trip_arcs, _graph: Graph):
    pull_out_node = Node("pull_out_" + _graph.commodity, 470, 0, 0)
    pull_in_node = Node("pull_in_" + _graph.commodity, 760, 0, 0)
    arc_return = Arc(pull_in_node, pull_out_node, 100, garage_tec_capacity, None)
    _graph.add_arc(arc_return)
    positioning_y = {}
    position = 50
    for trip in _trips:
        if positioning_y.get(trip.itinerary.origin, None) is None:
            positioning_y[trip.itinerary.origin] = position
            position = position + 50
        origin_node = Node(trip.itinerary.origin, trip.start_time, 1, positioning_y[trip.itinerary.origin])
        if positioning_y.get(trip.itinerary.destination, None) is None:
            positioning_y[trip.itinerary.destination] = position
            position = position + 50
        destination_node = Node(trip.itinerary.destination, trip.end_time, -1, positioning_y[trip.itinerary.destination])
        edge = Arc(origin_node, destination_node, cost=0, capacity=0, scheduling_event=trip)
        _graph.add_arc(edge)
        trip_arcs.append(edge)
        pull_out = Arc(destination_node, pull_in_node, 100, 1, "insert_deadhead_here")
        _graph.add_arc(pull_out)
        pull_in = Arc(pull_out_node, origin_node, 100, 1, "insert_deadhead_here")
        _graph.add_arc(pull_in)


def add_connection_arcs(garage_tec_capacity: int, _trip_arcs, _compatibility_rules, _graph: Graph):
    for i, trip_arc_i in enumerate(_trip_arcs):
        for j, trip_arc_j in enumerate(_trip_arcs):
            if i != j:
                event_between = _compatibility_rules.event_between(trip_arc_i.scheduling_event,
                                                                   trip_arc_j.scheduling_event)
                if event_between is not None:
                    origin_node = trip_arc_i.destination_node
                    destination_node = trip_arc_j.origin_node
                    edge = Arc(origin_node, destination_node, cost=event_between.end_time - event_between.start_time,
                               capacity=1, scheduling_event=event_between)
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
    graph = build_graph('garage1-common_vehicle', 10, trips, compatibility_rules)
    # network.arcs.sort(key=lambda _arc: _arc.origin_node.time)
    for node in graph.nodes:
        print(node)
    print("------------")
    for e in graph.arcs:
        print(e)
