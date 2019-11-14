from deal_with_time import minutes
from vehicle_scheduling.column_generation import pricing_problem
from vehicle_scheduling.column_generation.master_problem import SetPartitioning, Variable
from vehicle_scheduling.column_generation.pricing_problem import SubProblem
from vehicle_scheduling.data_model.compatible_trips_rules import CompatibilityRules, LayoverTime, PossibleDeadheads, \
    PossibleLineConnections
from vehicle_scheduling.data_model.scheduled_event import ScheduledTrip
from vehicle_scheduling.data_model.transport_network import Deadhead, Itinerary
from vehicle_scheduling.graph.building_connection_based_graph import build_graph
from vehicle_scheduling.graph.commodities_trips import Commodity


class BranchAndPrice:

    def __init__(self, commodities: list, compatibilities_rules: CompatibilityRules):
        self.commodities = commodities
        self.compatibility_rules = compatibilities_rules
        self.master_problem = None

    def execute(self):
        self.find_initial_solution()
        pricing_problems = self.initialize()
        while could_be_improved:
            sigma, pi = self.solve_master_problem()

    # pensar em como criar uma solução inicial independente da rede
    # será que preciso ter uma lista com os arcos referentes às viagens?
    # preciso
    def find_initial_solution(self) -> SetPartitioning:
        variables = []
        for commodity in self.commodities:
            for trip in commodity.trips:
                variables.append(Variable()) ###
        return SetPartitioning(variables, )


    def initialize(self):
        pricing_problems = []
        for commodity in self.commodities:
            graph = build_graph(commodity, self.compatibility_rules)
            problem = pricing_problem.SubProblem(commodity.commodity_name)
            problem.build_network(graph)
            pricing_problems.append(problem)
        return pricing_problems


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
    trips_garage1 = [trips1, trips2, trips3, trips4]
    trips_garage2 = trips_garage1

    # network_depot1 = build_graph(Commodity('garage1-vehicleType1', 2, trips_garage1), compatibility_rules)
    # network_depot2 = build_graph(Commodity('garage2-vehicleType1', 2, trips_garage2), compatibility_rules)
    # network.arcs.sort(key=lambda _arc: _arc.origin_node.time)
    # for arc in network.arcs:
    #     print(arc)

    # pricing_problem_depot1 = pricing_problem.SubProblem(network_depot1.commodity)
    # pricing_problem_depot2 = pricing_problem.SubProblem('Depot2')
    #
    # pricing_problem_depot1.build_network(network_depot1)
    # pricing_problem_depot2.build_network(network_depot2)
    # # pricing_problem_depot1.update_arc_costs()
    # pricing_problem_depot1.execute()
    # pricing_problem_depot2.execute()
    # pricing_problem_depot1.plot_network()
    # pricing_problem_depot2.plot_network()

    branch_and_price = BranchAndPrice([Commodity('garage1-vehicleType1', 2, trips_garage1),
                                       Commodity('garage2-vehicleType1', 2, trips_garage2)], compatibility_rules)

