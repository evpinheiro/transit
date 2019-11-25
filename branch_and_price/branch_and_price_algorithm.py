from branch_and_price import pricing
from branch_and_price.master import SetPartitioning, Variable


class BranchAndPrice:

    def __init__(self, commodities_graphs: list):
        self.commodities_graphs = commodities_graphs
        self.master_problem = None

    def execute(self):
        pricing_problems = self.initialize()
        self.find_initial_solution(pricing_problems)
        # while could_be_improved:
        #     sigma, pi = self.solve_master_problem()

    def find_initial_solution(self, princing_problems):
        initial_vars = {}
        for graph_commodity in self.commodities_graphs:
            initial_vars[graph_commodity.commodity_name] = Variable(100, graph_commodity.commodity_name, [])
        self.column_generation(SetPartitioning(initial_vars, self.all_trips_arcs), princing_problems)

    def initialize(self):
        pricing_problems = []
        for graph_commodity in self.commodities_graphs:
            problem = pricing.Pricing(graph_commodity.commodity_name)
            problem.build_network(graph_commodity)
            pricing_problems.append(problem)
        return pricing_problems

    def column_generation(self, master_problem, princing_problems):
        stop = False
        while not stop:
            master_problem.execute()
            sigma, pi = master_problem.get_dual()
            new_columns = self.update_and_solve_pricing_problems(sigma, pi, princing_problems)
            self.update_master_problem(master_problem, new_columns)

    def update_and_solve_pricing_problems(self, sigma, pi, princing_problems):
        for pricing in princing_problems:
            pricing.update_arc_costs(pi)


if __name__ == '__main__':
    ...
