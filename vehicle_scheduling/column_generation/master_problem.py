import pyomo.environ as pe
import pyomo as pyo
import logging


class Variable:

    def __init__(self, cost: int, commodity: str, scheduled_trips):
        # self.index = None
        self.cost = cost
        self.commodity = commodity
        self.scheduled_trips = scheduled_trips


class SetPartitioning:

    def __init__(self, initial_variables_by_commodity, scheduled_trips):
        logging.getLogger('pyomo.core').setLevel(logging.ERROR)
        self.solver = pyo.opt.SolverFactory('cbc')
        self.results = "NotExecuted"
        self.model = pe.ConcreteModel('master_problem')
        indexes = []
        self.cost_vector = {}
        for commodity in initial_variables_by_commodity.keys():
            for index, var in enumerate(initial_variables_by_commodity[commodity]):
                var.index = (commodity, str(index))
                indexes.append(var.index)
                self.cost_vector[var.index] = var.cost
        self.model.DK = indexes
        self.model.var_lambda = pe.Var(self.model.DK, domain=pe.NonNegativeReals)
        self.model.obj = pe.Objective(expr=sum(self.cost_vector[dk] * self.model.var_lambda[dk]
                                               for dk in self.model.DK), sense=pe.minimize)
        self.model.dual = pe.Suffix(direction=pe.Suffix.IMPORT)
        # self.model.rc = pe.Suffix(direction=pe.Suffix.IMPORT_EXPORT)
        self.set_partitioning_constraints(scheduled_trips, initial_variables_by_commodity)
        self.set_convexity_constraints(initial_variables_by_commodity)

    def add_upper_bound(self, var_index, bound_value):
        self.model.constraints.add(self.model.var_lambda[var_index] <= bound_value)

    def add_lower_bound(self, var_index, bound_value):
        self.model.constraints.add(self.model.var_lambda[var_index] >= bound_value)

    def set_partitioning_constraints(self, scheduled_trips: list, initial_variables_by_commodity):
        self.model.partitioning_constraint = pe.ConstraintList()
        for trip in scheduled_trips:
            self.model.partitioning_constraint.add(
                expr=sum(self.model.var_lambda[dk] for dk in self.model.DK
                         if initial_variables_by_commodity[dk[0]][int(dk[1])].scheduled_trips.__contains__(trip)) == 1)

    def set_convexity_constraints(self, initial_variables_by_commodity):
        self.model.convexity_constraint = pe.ConstraintList()
        for commodity in initial_variables_by_commodity.keys():
            self.model.convexity_constraint.add(
                expr=sum(self.model.var_lambda[dk] for dk in self.model.DK if dk[0] == commodity) == 1)

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
        return [self.model.var_lambda[dk]() for dk in self.model.DK]

    def evaluate_solution(self, solution):
        return sum(self.cost_vector[dk] * solution[dk] for dk in self.model.DK)

    def get_dual(self):
        if not self.is_feasible():
            return self.results.solver.status
        duals_by_constraint_by_class = {}
        for constraints in self.model.component_objects(pe.Constraint, active=True):
            constraint_class = constraints.name
            duals_by_constraint_by_class[constraint_class] = []
            for i, constraint in constraints.items():
                # name = constraint.name
                duals_by_constraint_by_class[constraint_class].insert(i, self.model.dual[constraint])
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
    lambda_k1_d1 = Variable(15, "D1", [trips[0], trips[1], trips[2]])
    lambda_k2_d1 = Variable(7, "D1", [trips[2]])
    lambda_k1_d2 = Variable(12, "D2", [trips[3], trips[4]])
    lambda_k2_d2 = Variable(8, "D2", [trips[3]])
    lambda_k3_d2 = Variable(5, "D2", [trips[4]])

    initial_vars = {"D1": [lambda_k1_d1, lambda_k2_d1], "D2": [lambda_k1_d2, lambda_k2_d2, lambda_k3_d2]}
    relax = SetPartitioning(initial_vars, trips)
    relax.execute()
    print('optimal solution: ', relax.get_solution())
    print('dual values:')
    for c in relax.get_dual().items():
        print(str(c))
