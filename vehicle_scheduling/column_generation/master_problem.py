import pyomo.environ as pe
import pyomo as pyo
import logging


class Variable:

    def __init__(self, cost: int, commodity):
        self.cost = cost
        self.commodity = commodity


class SetParticioning:

    def __init__(self, initial_variables: map[str], trips):
        logging.getLogger('pyomo.core').setLevel(logging.ERROR)
        self.solver = pyo.opt.SolverFactory('cbc')
        self.results = "NotExecuted"
        self.model = pe.ConcreteModel()

        self.model.J = range(initial_variables)
        self.model.x = pe.Var(self.model.J, domain=pe.NonNegativeReals)
        self.cost_vector = [v.cost for v in initial_variables]
        self.model.obj = pe.Objective(expr=sum(self.cost_vector[i] * self.model.x[i]
                                               for i in self.model.J), sense=pe.maximize)
        self.model.dual = pe.Suffix(direction=pe.Suffix.IMPORT)
        self.model.rc = pe.Suffix(direction=pe.Suffix.IMPORT_EXPORT)
        self.model.constraints = pe.ConstraintList()
        # self.model.constraints.add(expr=6.7*self.model.x[0] + 2 * self.model.x[1] <= 17)
        # self.model.constraints.add(expr=-2.5*self.model.x[0] + self.model.x[1] <= 2)
        self.model.constraint_row1 = pe.Constraint(expr=8 * self.model.x[0] + 2 * self.model.x[1] <= 17)
        self.model.constraint_row2 = pe.Constraint(expr=-self.model.x[0] + self.model.x[1] <= 2)

    def add_upper_bound(self, var_index, bound_value):
        self.model.constraints.add(self.model.x[var_index] <= bound_value)

    def add_lower_bound(self, var_index, bound_value):
        self.model.constraints.add(self.model.x[var_index] >= bound_value)

    def execute(self):
        self.results = self.solver.solve(self.model)
        # self.model.display()
        # self.model.dual.display()
        # self.model.rc.display()

    def is_feasible(self):
        return self.results.solver.status == pyo.opt.SolverStatus.ok

    def get_bound(self):
        return self.model.obj()

    def get_solution(self):
        return [self.model.x[j]() for j in self.model.J]

    def evaluate_solution(self, solution):
        return sum(self.cost_vector[i] * solution[i] for i in self.model.J)

    def get_dual(self):
        duals_by_constraint = {}
        for constraints in self.model.component_objects(pe.Constraint, active=True):
            if constraints.name != "constraints":
                duals_by_constraint[constraints.name] = self.model.dual[constraints]
        return duals_by_constraint

    def get_reduced_cost(self):
        rc = {}
        for var in self.model.component_objects(pe.Var, active=True):
            for i in var:
                rc[var[i].name] = self.model.rc[var[i]]
        return rc
