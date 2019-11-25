from branch_and_price.graph import Node, Arc, Graph

from branch_and_price.mincost_multicommodity_flow import multicommodity_minimum_cost_flow

# stations nodes
node_trip1_o = Node('trip1_origin')  # S1-08:00
node_trip1_d = Node('trip1_destination')  # S2-08:50
node_trip2_o = Node('trip2_origin')  # S2-09:00
node_trip2_d = Node('trip2_destination')  # S1-09:50
node_trip3_o = Node('trip3_origin')  # S1-09:00
node_trip3_d = Node('trip3_destination')  # S2-09:50
node_trip4_o = Node('trip4_origin')  # S2-10:00
node_trip4_d = Node('trip4_destination')  # S1-11:00
# depot nodes
node_pull_out_trip1 = Node('pull_out_trip1')
node_pull_in_trip1 = Node('pull_in_trip1')
node_pull_out_trip2 = Node('pull_out_trip2')
node_pull_in_trip2 = Node('pull_in_trip2')
node_pull_out_trip3 = Node('pull_out_trip3')
node_pull_in_trip3 = Node('pull_in_trip3')
node_pull_out_trip4 = Node('pull_out_trip4')
node_pull_in_trip4 = Node('pull_in_trip4')
# trip arcs
arc_trip1 = Arc(node_trip1_o, node_trip1_d, 1, 1)
arc_trip2 = Arc(node_trip2_o, node_trip2_d, 1, 1)
arc_trip3 = Arc(node_trip3_o, node_trip3_d, 1, 1)
arc_trip4 = Arc(node_trip4_o, node_trip4_d, 1, 1)
# pull-out pull-in arcs
arc_pull_out_trip1 = Arc(node_pull_out_trip1, node_trip1_o, 2)
arc_pull_in_trip1 = Arc(node_trip1_d, node_pull_in_trip1, 2)
arc_pull_out_trip2 = Arc(node_pull_out_trip2, node_trip2_o, 2)
arc_pull_in_trip2 = Arc(node_trip2_d, node_pull_in_trip2, 2)
arc_pull_out_trip3 = Arc(node_pull_out_trip3, node_trip3_o, 2)
arc_pull_in_trip3 = Arc(node_trip3_d, node_pull_in_trip3, 2)
arc_pull_out_trip4 = Arc(node_pull_out_trip4, node_trip4_o, 2)
arc_pull_in_trip4 = Arc(node_trip4_d, node_pull_in_trip4, 2)
# deadhead trip arcs
arc_trip1d_trip3o = Arc(node_trip1_d, node_trip3_o, 2)
arc_trip2d_trip4o = Arc(node_trip2_d, node_trip4_o, 2)
# deadhead time in station
arc_trip1d_trip2o = Arc(node_trip1_d, node_trip2_o, 2)
arc_trip3d_trip4o = Arc(node_trip3_d, node_trip4_o, 2)
# deadhead time in garage
arc_depot_standing1 = Arc(node_pull_out_trip1, node_pull_in_trip1, 2)
arc_depot_standing2 = Arc(node_pull_in_trip1, node_pull_out_trip3, 2)
arc_depot_standing3 = Arc(node_pull_out_trip3, node_pull_out_trip2, 2)
arc_depot_standing4 = Arc(node_pull_out_trip2, node_pull_in_trip3, 2)
arc_depot_standing5 = Arc(node_pull_in_trip3, node_pull_out_trip4, 2)
arc_depot_standing6 = Arc(node_pull_out_trip4, node_pull_in_trip2, 2)
arc_depot_standing7 = Arc(node_pull_in_trip2, node_pull_in_trip4, 2)
# returning arc
arc_returning = Arc(node_pull_in_trip4, node_pull_out_trip1, 1)

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
                 arc_depot_standing7: (1, 2), arc_returning: (1, 2)})

graph_2 = Graph('2', {node_trip1_o: 0, node_trip1_d: 0, node_trip2_o: 0, node_trip2_d: 0,
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
                 arc_depot_standing7: (1, 2), arc_returning: (1, 2)})

graph_list = [graph_1, graph_2]

multicommodity_minimum_cost_flow(graph_list,
                                 [arc_trip1, arc_trip2, arc_trip3, arc_trip4],
                                 False)
