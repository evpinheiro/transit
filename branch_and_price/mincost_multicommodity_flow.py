import pyomo.opt
import pyomo.environ as pe
from pyomo.core import value

from branch_and_price.graph import Node, Arc, Graph, ArcType
from deal_with_time import minutes


def multicommodity_minimum_cost_flow(graphs: list, common_arcs: list, integer: bool):
    modelo = pe.ConcreteModel(name="MCFP")

    modelo.dual = pe.Suffix(direction=pe.Suffix.IMPORT)

    commodities_arcs = {(graph_k.commodity_name, str(arc[0])):
                            arc for graph_k in graphs for arc in graph_k.arcs_cost_cap.items()}
    modelo.var_indexes = commodities_arcs.keys()
    modelo.var = pe.Var(modelo.var_indexes, within=pe.NonNegativeIntegers if integer else pe.NonNegativeReals)

    def objetivo(m):
        return sum(commodities_arcs[index][1][0] * m.var[index] for index in modelo.var_indexes)

    modelo.obj = pe.Objective(rule=objetivo, sense=pe.minimize)

    commodities_nodes = [(commodity, node) for commodity in graphs for node in commodity.nodes_demands.items()]

    def conserva_fluxo(m, index):
        commodity, node = commodities_nodes[index]
        from_i = [str(arc) for arc in commodity.arcs_cost_cap.keys() if arc.origin == node[0]]
        to_i = [str(arc) for arc in commodity.arcs_cost_cap.keys() if arc.destination == node[0]]
        return sum(m.var[(commodity.commodity_name, v)] for v in from_i) - sum(
            m.var[(commodity.commodity_name, v)] for v in to_i) == node[1]

    modelo.commodities_nodes_indexes = range(len(commodities_nodes))
    modelo.flow_conservation = pe.Constraint(modelo.commodities_nodes_indexes, rule=conserva_fluxo)

    def capacidades_conjuntas(m, index):
        soma = sum(m.var[(commodity.commodity_name, str(common_arcs[index]))] for commodity in graphs
                   if (commodity.commodity_name, str(common_arcs[index])) in modelo.var_indexes)
        return soma <= common_arcs[index].capacity

    modelo.capacidade_conjunta_arco = pe.Constraint(range(len(common_arcs)), rule=capacidades_conjuntas)

    def lower_bound_conjuntas(m, index):
        soma = sum(m.var[(commodity.commodity_name, str(common_arcs[index]))] for commodity in graphs
                   if (commodity.commodity_name, str(common_arcs[index])) in modelo.var_indexes)
        return common_arcs[index].lower_bound <= soma

    modelo.lower_bound_conjunta_arco = pe.Constraint(range(len(common_arcs)), rule=lower_bound_conjuntas)

    def capacidades(m, commodity, arc):
        var_index = (commodity, arc)
        return m.var[var_index] <= commodities_arcs.get(var_index)[1][1]

    modelo.capacidade = pe.Constraint(modelo.var_indexes, rule=capacidades)

    solver = pyomo.opt.SolverFactory('cbc')
    results = solver.solve(modelo)
    modelo.display()
    # modelo.pprint()

    print(results.solver.status)
    for dk in modelo.var_indexes:
        if modelo.var[dk].value > 0:
            print(dk, modelo.var[dk].value)

    print(modelo.obj())


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
                 arc_depot_standing7: (1, 2), arc_returning: (10, 1)})

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
                 arc_depot_standingD: (1, 2), arc_depot_standingE: (1, 2), arc_returning: (10, 1)})

graph_list = [graph_1, graph_2]

multicommodity_minimum_cost_flow(graph_list,
                                 [arc_trip1, arc_trip2, arc_trip3, arc_trip4],
                                 True)


# arc12 = Arc(node1, node2, 5)
# arc14 = Arc(node1, node4, 5)
# arc23 = Arc(node2, node3, 5)
# arc31 = Arc(node3, node1, 5)
# arc42 = Arc(node4, node2, 5)
# arc43 = Arc(node4, node3, 5)
#
# graph_32 = Graph('3-2', {node1: 0, node2: -4, node3: 4, node4: 0},
#                  {arc12: (2, 5), arc14: (1, 5), arc23: (1, 5), arc31: (1, 5), arc43: (1, 5), arc42: (1, 5)})
# graph_13 = Graph('1-3', {node1: 4, node2: 0, node3: -4, node4: 0},
#                  {arc12: (1, 5), arc14: (2, 5), arc23: (1, 5), arc31: (1, 5), arc43: (2, 5), arc42: (4, 5)})
# graph_24 = Graph('2-4', {node1: 0, node2: 1, node3: 0, node4: -1},
#                  {arc12: (1, 5), arc14: (2, 5), arc23: (1, 5), arc31: (1, 5), arc43: (2, 5), arc42: (4, 5)})

# graph_list = [graph_32, graph_13, graph_24]


# s1 = Node('s1')
# t1 = Node('t1')
# s2 = Node('s2')
# t2 = Node('t2')
# node1 = Node(1)
# node2 = Node(2)
# node3 = Node(3)
# node4 = Node(4)
#
# arc_s1_1 = Arc(s1, node1, 1)
# arc_1_2 = Arc(node1, node2, 1)
# arc_2_t2 = Arc(node2, t2, 1)
# arc_1_3 = Arc(node1, node3, 1)
# arc_3_2 = Arc(node3, node2, 1)
# arc_3_t1 = Arc(node3, t1, 1)
# arc_4_3 = Arc(node4, node3, 1)
# arc_4_1 = Arc(node4, node1, 1)
# arc_2_4 = Arc(node2, node4, 1)
# arc_s2_4 = Arc(s2, node4, 1)
#
# graph_1 = Graph('s1-t1', {s1: 1, t1: -1, s2: 0, t2: 0, node1: 0, node2: 0, node3: 0, node4: 0},
#                 {arc_s1_1: (1, 5), arc_1_2: (1, 5), arc_2_t2: (1, 5), arc_1_3: (5, 5), arc_3_2: (1, 5),
#                  arc_3_t1: (1, 5), arc_4_3: (1, 5), arc_4_1: (1, 5), arc_2_4: (1, 5), arc_s2_4: (1, 5)})
# graph_2 = Graph('s2-t2', {s1: 0, t1: 0, s2: 1, t2: -1, node1: 0, node2: 0, node3: 0, node4: 0},
#                 {arc_s1_1: (1, 5), arc_1_2: (1, 5), arc_2_t2: (1, 5), arc_1_3: (1, 5), arc_3_2: (1, 5),
#                  arc_3_t1: (1, 5), arc_4_3: (1, 5), arc_4_1: (1, 5), arc_2_4: (1, 5), arc_s2_4: (1, 5)})
