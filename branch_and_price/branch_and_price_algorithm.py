from branch_and_price import pricing
from branch_and_price.graph import Node, Arc, Graph, ArcType
from branch_and_price.master import SetPartitioning, Variable, ConstraintType
from deal_with_time import minutes


class BranchAndPrice:

    def __init__(self, commodities_graphs: list, all_trips_arc: list, first_basic_solution=None):
        self.all_trips_arcs_codes = all_trips_arc  # TODO getting the trips from the graphs
        self.commodities_graphs = commodities_graphs
        self.all_columns = []
        self.master_problem = first_basic_solution

    def execute(self):
        pricing_problems = self.initialize()
        if self.master_problem is None:
            self.all_columns = self.find_initial_solution(pricing_problems)
            self.update_master_problem()
        else:
            self.master_problem.execute()
            self.all_columns.extend(self.master_problem.get_solution())
        self.column_generation(pricing_problems)
        # could_be_improved = True
        # while could_be_improved:
        #     sigma, pi = self.solve_master_problem()
        result = self.master_problem.get_solution()
        for var in result:
            var.paths.sort(key=lambda arc: arc.origin.time)
            print(var.value, var.commodity, [arc.get_code() for arc in var.paths])

    def find_initial_solution(self, princing_problems):
        initial_vars = self.get_artificial_variables()
        self.master_problem = SetPartitioning(initial_vars, self.all_trips_arcs_codes)
        self.column_generation(princing_problems)
        result = self.master_problem.get_solution()
        return result

    def get_artificial_variables(self):
        initial_vars = {}
        for graph_commodity in self.commodities_graphs:
            variable = Variable(100, graph_commodity.commodity_name, [], None)
            initial_vars[graph_commodity.commodity_name] = [variable]
            self.all_columns.append(variable)
        for i, trip_arc in enumerate(self.all_trips_arcs_codes):
            variable = Variable(100, "-" + str(i), [trip_arc], None)
            if initial_vars.get("-" + str(i)) is None:
                initial_vars["-" + str(i)] = [variable]
            else:
                initial_vars["-" + str(i)].append(variable)
            self.all_columns.append(variable)
        return initial_vars

    def initialize(self):
        pricing_problems = []
        for graph_commodity in self.commodities_graphs:
            problem = pricing.Pricing(graph_commodity.commodity_name)
            problem.build_network(graph_commodity)
            pricing_problems.append(problem)
        return pricing_problems

    def column_generation(self, princing_problems):
        stop = False
        while not stop:
            duals_by_constraint_by_class = self.master_problem.get_dual()
            sigma = duals_by_constraint_by_class.get(ConstraintType.CONVEXITY.value)
            pi = duals_by_constraint_by_class.get(ConstraintType.PARTITIONING.value)
            new_columns = self.update_and_solve_pricing_problems(sigma, pi, princing_problems)
            if len(new_columns) > 0:
                self.all_columns.extend(new_columns)
                self.update_master_problem()
                self.master_problem.execute()
            else:
                stop = True

    def update_and_solve_pricing_problems(self, sigma, pi, princing_problems):
        new_columns = []
        for pricing in princing_problems:
            pricing.update_arc_costs(pi)
            pricing.execute()
            pricing.print_solution()
            if -sigma[pricing.network.name] + pricing.total_cost < 0:
                new_columns.append(
                    self.build_new_column(pricing.network.name,
                                          pricing.get_original_cost(),
                                          pricing.get_solution_trips_arcs_codes(),
                                          pricing.get_solution_all_arcs()))
                # print(pricing.network.name, pricing.path_scheduled_trips_arcs)
        return new_columns

    def build_new_column(self, commodity_name, original_cost, scheduled_trips_codes, path_all_arcs):
        return Variable(original_cost, commodity_name, scheduled_trips_codes, path_all_arcs)

    def update_master_problem(self):
        var_by_commodity = {}
        for var in self.all_columns:
            if var_by_commodity.get(var.commodity) is None:
                var_by_commodity[var.commodity] = [var]
            else:
                var_by_commodity[var.commodity].append(var)
        self.master_problem = SetPartitioning(var_by_commodity, self.all_trips_arcs_codes)


if __name__ == '__main__':
    # stations nodes
    node_trip1_o = Node('trip1_origin', 1, minutes("08:00"))  # S1-08:00
    node_trip1_d = Node('trip1_destination', 2, minutes('08:50'))  # S2-08:50
    node_trip2_o = Node('trip2_origin', 2, minutes('09:00'))  # S2-09:00
    node_trip2_d = Node('trip2_destination', 1, minutes('09:50'))  # S1-09:50
    node_trip3_o = Node('trip3_origin', 1, minutes('09:00'))  # S1-09:00
    node_trip3_d = Node('trip3_destination', 2, minutes('09:50'))  # S2-09:50
    node_trip4_o = Node('trip4_origin', 2, minutes('10:00'))  # S2-10:00
    node_trip4_d = Node('trip4_destination', 1, minutes('11:00'))  # S1-11:00
    # depot nodes
    node_pull_out_trip1 = Node('pull_out_trip1', 0, minutes('07:50'))
    node_pull_in_trip1 = Node('pull_in_trip1', 0, minutes('09:00'))
    node_pull_out_trip2 = Node('pull_out_trip2', 0, minutes('08:55'))
    node_pull_in_trip2 = Node('pull_in_trip2', 0, minutes('10:00'))
    node_pull_out_trip3 = Node('pull_out_trip3', 0, minutes('08:55'))
    node_pull_in_trip3 = Node('pull_in_trip3', 0, minutes('09:55'))
    node_pull_out_trip4 = Node('pull_out_trip4', 0, minutes('09:55'))
    node_pull_in_trip4 = Node('pull_in_trip4', 0, minutes('11:10'))
    # trip arcs
    arc_trip1 = Arc(ArcType.TRIP, node_trip1_o, node_trip1_d, 1, 1)
    arc_trip2 = Arc(ArcType.TRIP, node_trip2_o, node_trip2_d, 1, 1)
    arc_trip3 = Arc(ArcType.TRIP, node_trip3_o, node_trip3_d, 1, 1)
    arc_trip4 = Arc(ArcType.TRIP, node_trip4_o, node_trip4_d, 1, 1)
    # pull-out pull-in arcs
    arc_pull_out_trip1 = Arc(ArcType.PULL_OUT, node_pull_out_trip1, node_trip1_o, 2)
    arc_pull_in_trip1 = Arc(ArcType.PULL_IN, node_trip1_d, node_pull_in_trip1, 2)
    arc_pull_out_trip2 = Arc(ArcType.PULL_OUT, node_pull_out_trip2, node_trip2_o, 2)
    arc_pull_in_trip2 = Arc(ArcType.PULL_IN, node_trip2_d, node_pull_in_trip2, 2)
    arc_pull_out_trip3 = Arc(ArcType.PULL_OUT, node_pull_out_trip3, node_trip3_o, 2)
    arc_pull_in_trip3 = Arc(ArcType.PULL_IN, node_trip3_d, node_pull_in_trip3, 2)
    arc_pull_out_trip4 = Arc(ArcType.PULL_OUT, node_pull_out_trip4, node_trip4_o, 2)
    arc_pull_in_trip4 = Arc(ArcType.PULL_IN, node_trip4_d, node_pull_in_trip4, 2)
    # deadhead trip arcs
    arc_trip1d_trip3o = Arc(ArcType.DEADHEAD_TRIP, node_trip1_d, node_trip3_o, 2)
    arc_trip2d_trip4o = Arc(ArcType.DEADHEAD_TRIP, node_trip2_d, node_trip4_o, 2)
    # deadhead time in station
    arc_trip1d_trip2o = Arc(ArcType.STOPPED, node_trip1_d, node_trip2_o, 2)
    arc_trip3d_trip4o = Arc(ArcType.STOPPED, node_trip3_d, node_trip4_o, 2)
    # deadhead time in garage
    arc_depot_standing1 = Arc(ArcType.STOPPED, node_pull_out_trip1, node_pull_in_trip1, 2)
    arc_depot_standing2 = Arc(ArcType.STOPPED, node_pull_in_trip1, node_pull_out_trip3, 2)
    arc_depot_standing3 = Arc(ArcType.STOPPED, node_pull_out_trip3, node_pull_out_trip2, 2)
    arc_depot_standing4 = Arc(ArcType.STOPPED, node_pull_out_trip2, node_pull_in_trip3, 2)
    arc_depot_standing5 = Arc(ArcType.STOPPED, node_pull_in_trip3, node_pull_out_trip4, 2)
    arc_depot_standing6 = Arc(ArcType.STOPPED, node_pull_out_trip4, node_pull_in_trip2, 2)
    arc_depot_standing7 = Arc(ArcType.STOPPED, node_pull_in_trip2, node_pull_in_trip4, 2)
    # returning arc
    arc_returning = Arc(ArcType.CIRCULATION, node_pull_in_trip4, node_pull_out_trip1, 1)

    graph_1 = Graph('1', {node_trip1_o: 0, node_trip1_d: 0, node_trip2_o: 0, node_trip2_d: 0,
                          node_trip3_o: 0, node_trip3_d: 0, node_trip4_o: 0, node_trip4_d: 0,
                          node_pull_out_trip1: 0, node_pull_in_trip1: 0, node_pull_out_trip2: 0,
                          node_pull_in_trip2: 0, node_pull_out_trip3: 0, node_pull_in_trip3: 0,
                          node_pull_out_trip4: 0, node_pull_in_trip4: 0},
                    {arc_trip1: (1, 1), arc_trip2: (1, 1), arc_trip3: (1, 1), arc_trip4: (1, 1),
                     arc_pull_out_trip1: (1, 2), arc_pull_in_trip1: (1, 2), arc_pull_out_trip2: (1, 2),
                     arc_pull_in_trip2: (1, 2), arc_pull_out_trip3: (1, 2), arc_pull_in_trip3: (1, 2),
                     arc_pull_out_trip4: (1, 2), arc_pull_in_trip4: (1, 2),
                     arc_trip1d_trip3o: (1, 2), arc_trip2d_trip4o: (1, 2),
                     arc_trip1d_trip2o: (1, 2), arc_trip3d_trip4o: (1, 2),
                     arc_depot_standing1: (1, 2), arc_depot_standing2: (1, 2), arc_depot_standing3: (1, 2),
                     arc_depot_standing4: (1, 2), arc_depot_standing5: (1, 2), arc_depot_standing6: (1, 2),
                     arc_depot_standing7: (1, 2), arc_returning: (1, 1)})

    arc_depot_standingA = Arc(ArcType.STOPPED, node_pull_out_trip1, node_pull_in_trip1, 2)
    arc_depot_standingB = Arc(ArcType.STOPPED, node_pull_in_trip1, node_pull_out_trip3, 2)
    arc_depot_standingC = Arc(ArcType.STOPPED, node_pull_out_trip3, node_pull_in_trip3, 2)
    arc_depot_standingD = Arc(ArcType.STOPPED, node_pull_in_trip3, node_pull_out_trip4, 2)
    arc_depot_standingE = Arc(ArcType.STOPPED, node_pull_out_trip4, node_pull_in_trip4, 2)

    graph_2 = Graph('2', {node_trip1_o: 0, node_trip1_d: 0,
                          node_trip3_o: 0, node_trip3_d: 0, node_trip4_o: 0, node_trip4_d: 0,
                          node_pull_out_trip1: 0, node_pull_in_trip1: 0, node_pull_out_trip3: 0, node_pull_in_trip3: 0,
                          node_pull_out_trip4: 0, node_pull_in_trip4: 0},
                    {arc_trip1: (1, 1), arc_trip3: (1, 1), arc_trip4: (1, 1),
                     arc_pull_out_trip1: (1, 2), arc_pull_in_trip1: (1, 2), arc_pull_out_trip3: (1, 2),
                     arc_pull_in_trip3: (1, 2), arc_pull_out_trip4: (1, 2), arc_pull_in_trip4: (1, 2),
                     arc_trip1d_trip3o: (1, 2), arc_trip3d_trip4o: (1, 2),
                     arc_depot_standingA: (1, 2), arc_depot_standingB: (1, 2), arc_depot_standingC: (1, 2),
                     arc_depot_standingD: (1, 2), arc_depot_standingE: (1, 2), arc_returning: (1, 1)})

    first_var_graph1 = Variable(9, '1', [arc_trip1.get_code(), arc_trip3.get_code()],
                                [arc_pull_out_trip1, arc_trip1, arc_trip1d_trip3o, arc_trip2, arc_pull_in_trip3,
                                 arc_depot_standing5, arc_depot_standing6, arc_depot_standing7, arc_returning])

    first_var_graph2 = Variable(9, '2', [arc_trip2.get_code(), arc_trip4.get_code()],
                                [arc_depot_standing1, arc_depot_standing2, arc_depot_standing3, arc_pull_out_trip2,
                                 arc_trip2, arc_trip2d_trip4o, arc_pull_in_trip4, arc_returning])

    first_basic_solution = SetPartitioning({'1': [first_var_graph1], '2': [first_var_graph2]},
        [arc_trip1.get_code(), arc_trip2.get_code(), arc_trip3.get_code(), arc_trip4.get_code()])

    branch_and_price = BranchAndPrice([graph_1, graph_2],
                                      [arc_trip1.get_code(), arc_trip2.get_code(),
                                       arc_trip3.get_code(), arc_trip4.get_code()],
                                      first_basic_solution)
    branch_and_price.execute()
