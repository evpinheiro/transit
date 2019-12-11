from enum import Enum

import pyomo.environ as pe
import pyomo as pyo
import logging


class Variable:

    def __init__(self, cost: int, commodity: str, scheduled_trips, arc_paths):
        # self.index = None
        self.cost = cost
        self.commodity = commodity
        self.scheduled_trips = scheduled_trips
        self.paths = arc_paths
        self.value = None


class ConstraintType(Enum):
    PARTITIONING = 'partitioning_constraint'
    CONVEXITY = 'convexity_constraint'


class SetPartitioning:

    def __init__(self, variables_by_commodity, scheduled_trips):
        logging.getLogger('pyomo.core').setLevel(logging.ERROR)
        self.solver = pyo.opt.SolverFactory('cbc')
        self.results = 'NotExecuted'
        self.model = pe.ConcreteModel('master_problem')
        indexes = []
        self.cost_vector = {}
        self.variables = {}
        self.commodities = []
        for commodity in variables_by_commodity.keys():
            self.commodities.append(commodity)
        for commodity in self.commodities:
            for index, var in enumerate(variables_by_commodity[commodity]):
                index = (commodity, str(index))
                indexes.append(index)
                self.variables[index] = var
                self.cost_vector[index] = var.cost
        self.model.DK = indexes
        self.model.var_lambda = pe.Var(self.model.DK, domain=pe.NonNegativeReals)
        self.model.obj = pe.Objective(expr=sum(self.cost_vector[dk] * self.model.var_lambda[dk]
                                               for dk in self.model.DK), sense=pe.minimize)
        self.model.dual = pe.Suffix(direction=pe.Suffix.IMPORT)
        # self.model.rc = pe.Suffix(direction=pe.Suffix.IMPORT_EXPORT)
        self.scheduled_trips = scheduled_trips
        self.set_partitioning_constraints(variables_by_commodity)
        self.set_convexity_constraints()

    def add_upper_bound(self, var_index, bound_value):
        self.model.constraints.add(self.model.var_lambda[var_index] <= bound_value)

    def add_lower_bound(self, var_index, bound_value):
        self.model.constraints.add(self.model.var_lambda[var_index] >= bound_value)

    def set_partitioning_constraints(self, initial_variables_by_commodity):
        self.model.partitioning_constraint = pe.ConstraintList()
        for trip in self.scheduled_trips:
            the_sum = sum(self.model.var_lambda[dk] for dk in self.model.DK
                          if initial_variables_by_commodity[dk[0]][int(dk[1])].scheduled_trips.__contains__(trip))
            if type(the_sum) is not int:
                self.model.partitioning_constraint.add(
                    expr=the_sum == 1)

    def set_convexity_constraints(self):
        self.model.convexity_constraint = pe.ConstraintList()
        for commodity in self.commodities:
            if int(commodity) > 0:  # TODO não depender desse código
                self.model.convexity_constraint.add(
                    expr=sum(self.model.var_lambda[dk] for dk in self.model.DK if dk[0] == commodity) == 1)

    def add_new_variable(self, variable):
        pass

    def execute(self):
        self.results = self.solver.solve(self.model)
        self.model.convexity_constraint.pprint()
        self.model.partitioning_constraint.pprint()

        self.model.display()
        # self.model.dual.display()
        # self.model.rc.display()

    def is_feasible(self):
        return self.results.solver.status == pyo.opt.SolverStatus.ok

    def get_bound(self):
        return self.model.obj()

    def get_solution(self):
        if not self.is_feasible():
            return self.results.solver.status
        for dk in self.model.DK:
            self.variables[dk].value = self.model.var_lambda[dk]()
        return [self.variables[dk] for dk in self.model.DK if self.model.var_lambda[dk]() > 0]

    def evaluate_solution(self, solution):
        return sum(self.cost_vector[dk] * solution[dk] for dk in self.model.DK)

    def get_dual(self):
        if not self.is_feasible():
            return self.results.solver.status
        duals_by_constraint_by_class = {}
        for constraints in self.model.component_objects(pe.Constraint, active=True):
            constraint_class = constraints.name
            duals_by_constraint_by_class[constraint_class] = {}
            for i, constraint in constraints.items():
                duals_by_constraint_by_class[constraint_class][
                    self.scheduled_trips[i - 1] if constraint_class == ConstraintType.PARTITIONING.value
                    else self.commodities[i - 1]] = self.model.dual[constraint]
        return duals_by_constraint_by_class

    def get_reduced_cost(self):
        if not self.is_feasible():
            return self.results.solver.status
        rc = {}
        for var in self.model.component_objects(pe.Var, active=True):
            for i in var:
                rc[var[i].name] = self.model.rc[var[i]]
        return rc


if __name__ == '__main__':
    trips = ['trip1', 'trip2', 'trip3', 'trip4', 'trip5']
    lambda_k1_d1 = Variable(0, "D1", [], [])
    lambda_k2_d1 = Variable(23, "D1", [trips[1], trips[2], trips[3]], [])
    lambda_k3_d1 = Variable(14, "D1", [trips[0], trips[1]], [])
    lambda_k1_d2 = Variable(33, "D2", [trips[0], trips[1], trips[2], trips[3], trips[4]], [])
    lambda_k2_d2 = Variable(12, "D2", [trips[3], trips[4]], [])
    lambda_k3_d2 = Variable(11, "D2", [trips[0], trips[4]], [])

    # trips = ['trip1', 'trip2', 'trip3', 'trip4']
    # lambda_k0_d1 = Variable(0, "D1", [])
    # lambda_k1_d1 = Variable(23, "D1", [trips[0]])
    # lambda_k2_d1 = Variable(14, "D1", [trips[1]])
    # lambda_k3_d1 = Variable(14, "D1", [trips[2]])
    # lambda_k4_d1 = Variable(14, "D1", [trips[3]])
    # lambda_k1_d2 = Variable(33, "D2", [trips[0]])
    # lambda_k2_d2 = Variable(12, "D2", [trips[1]])
    # lambda_k3_d2 = Variable(11, "D2", [trips[2]])
    # lambda_k4_d2 = Variable(11, "D2", [trips[3]])

    # initial_vars = {"D2": [lambda_k1_d2, lambda_k2_d2, lambda_k3_d2],
    #                 "D1": [lambda_k1_d1, lambda_k2_d1, lambda_k3_d1]}
    #
    # relax = SetPartitioning(initial_vars, trips)

    initial_vars = {"2": [Variable(100, "2", [], [])],
                    "1": [Variable(100, "1", [], [])]}
    relax = SetPartitioning(initial_vars, trips)

    relax.execute()
    print('optimal solution: ', relax.get_solution())
    print('dual values:')
    for c in relax.get_dual().items():
        print(str(c))
