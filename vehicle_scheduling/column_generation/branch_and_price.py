from deal_with_time import minutes
from vehicle_scheduling.column_generation import pricing_problem
from vehicle_scheduling.data_model.compatible_trips_rules import CompatibilityRules, LayoverTime, PossibleDeadheads, \
    PossibleLineConnections
from vehicle_scheduling.data_model.scheduled_event import ScheduledTrip
from vehicle_scheduling.data_model.transport_network import Deadhead, Itinerary
from vehicle_scheduling.graph.building_connection_based_graph import build_graph


class BranchAndPrice:

    def __init__(self, pricing_problems: list):
        self.sub_problems = pricing_problems
        print("*-------------*")
        for element in self.sub_problems:
            print(element.network)
            print("-------------")
        print("*-------------*")


if __name__ == '__main__':
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
    network_depot1 = build_graph('garage1-vehicleType1', 2, trips, compatibility_rules)
    network_depot2 = build_graph('garage2-vehicleType1', 2, trips, compatibility_rules)
    # network.arcs.sort(key=lambda _arc: _arc.origin_node.time)
    # for arc in network.arcs:
    #     print(arc)

    subproblem_depot1 = pricing_problem.Subproblem('Depot1')
    subproblem_depot2 = pricing_problem.Subproblem('Depot2')

    subproblem_depot1.build_network(network_depot1)
    subproblem_depot2.build_network(network_depot2)
    # subproblem_depot1.update_arc_costs()
    subproblem_depot1.execute()
    subproblem_depot2.execute()
    # subproblem_depot1.plot_network()
    # subproblem_depot2.plot_network()

    branch_and_price = BranchAndPrice([subproblem_depot1, subproblem_depot2])

