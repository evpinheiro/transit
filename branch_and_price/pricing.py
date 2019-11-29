import networkx as nx
import matplotlib.pyplot as plt

from branch_and_price.graph import Graph, Arc, Node, ArcType
from deal_with_time import minutes


class Pricing:

    def __init__(self, garage_vehicle_type_name):
        self.network = nx.DiGraph(name=garage_vehicle_type_name)
        self.arcs_values = {}
        self.total_cost = 0
        self.original_total_cost = 0
        self.solution = None
        self.arc_original_weight = {}
        self.paths_solution_arcs = []
        self.path_solution_trip_arcs_codes = []

    def build_network(self, graph: Graph):
        for node in graph.nodes_demands.items():
            self.network.add_node(node[0].code, demand=node[1],
                                  pos=(node[0].time * 1000, node[0].location))
        for arc in graph.arcs_cost_cap.items():
            self.arc_original_weight[arc[0].origin.code + "-" + arc[0].destination.code] = arc[1][0]
            self.network.add_edge(arc[0].origin.code, arc[0].destination.code, weight=arc[1][0],
                                  capacity=arc[1][1], original_events=arc, color='black')
            # if arc[1][1] == 0:
            #     self.trip_arcs.append(arc[0])

    def update_arc_costs(self, trips_arcs_reduced_costs: dict):
        new_weights = {}
        for trip_arc in trips_arcs_reduced_costs.items():
            origin, destination = trip_arc[0].split('-')
            if self.arc_original_weight.get(trip_arc[0]) is not None:
                new_weights[(origin, destination)] = self.arc_original_weight.get(trip_arc[0]) - trip_arc[1]
        # self.network[origin_code][destination_code]['weight'] = self.arc_original_weight[trip_arc[0]] - trip_arc[1]
        nx.set_edge_attributes(self.network, new_weights, 'weight')
        # node_attributes = nx.get_node_attributes(self.network, 'demand')
        # for e in self.network.nodes:
        #     # print(self.network[e[0]][e[1]]['original_events'])
        #     # print(e[0], e[1])
        #     print(e, node_attributes[e])
        # print("------------------")
        # for e in self.network.edges:
        #     print(self.network[e[0]][e[1]]['original_events'])
        # print("------------------")

    def execute(self):
        solution = nx.min_cost_flow(self.network)
        self.solution = solution
        self.total_cost = 0
        self.original_total_cost = 0
        self.path_solution_trip_arcs_codes = []
        self.paths_solution_arcs = []
        for node_origen in self.solution.keys():
            for node_destination in self.solution[node_origen].keys():
                self.arcs_values[node_origen + "-" + node_destination] = \
                    self.network.get_edge_data(node_origen, node_destination)
                if self.solution[node_origen][node_destination] > 0:
                    self.paths_solution_arcs.append(self.network[node_origen][node_destination]['original_events'][0])
                    if self.network[node_origen][node_destination]['original_events'][0].arc_type == ArcType.TRIP:
                        self.path_solution_trip_arcs_codes.append(
                            self.network[node_origen][node_destination]['original_events'][0].get_code())
                self.total_cost += self.solution[node_origen][node_destination] * \
                                   self.network.get_edge_data(node_origen, node_destination)['weight']
                self.original_total_cost = self.solution[node_origen][node_destination] * \
                                           self.arc_original_weight[node_origen + "-" + node_destination]

    def get_solution_trips_arcs_codes(self):
        return self.path_solution_trip_arcs_codes.copy()

    def get_solution_all_arcs(self):
        return self.paths_solution_arcs.copy()

    def get_original_cost(self):
        return self.original_total_cost

    def print_solution(self):
        print("----------------- networkx o-d | original event | cost ------------------")
        for node_origen in self.solution.keys():
            for node_destination in self.solution[node_origen].keys():
                print(node_origen, node_destination, "|",
                      self.network[node_origen][node_destination]['original_events'], "|",
                      self.solution[node_origen][node_destination], "|",
                      self.network.get_edge_data(node_origen, node_destination))
        print("-------------- solution arcs -----------------")
        total_cost = 0
        for node_origen in self.solution.keys():
            for node_destination in self.solution[node_origen].keys():
                if self.solution[node_origen][node_destination] > 0 \
                        or self.network[node_origen][node_destination]['capacity'] == 0:
                    print(node_origen, node_destination, "|",
                          self.network[node_origen][node_destination]['original_events'], "|",
                          self.solution[node_origen][node_destination], "|",
                          self.network.get_edge_data(node_origen, node_destination))
                    self.network[node_origen][node_destination]['color'] = 'red' \
                        if self.solution[node_origen][node_destination] > 0 else 'green'
                total_cost += self.solution[node_origen][node_destination] * \
                              self.network.get_edge_data(node_origen, node_destination)['weight']
        print("--------------------Total Cost---------------")
        print(total_cost)
        print("---------------------------------------------")

    def plot_network(self):
        edge_labels = {}
        pos = nx.get_node_attributes(self.network, 'pos')
        color_edges = [self.network[u][v]['color'] for u, v in self.network.edges]
        nx.draw(self.network, pos, edges=self.network.edges, edge_color=color_edges, with_labels=True, node_size=50,
                alpha=0.7, arrows=True, font_size=8, arrowsize=11)
        labels_return = nx.draw_networkx_edge_labels(self.network, pos, edge_labels=edge_labels, font_size=9)
        plt.show()


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
    arc_returning = Arc(ArcType.CIRCULATION, node_pull_in_trip4, node_pull_out_trip1, 2)

    graph_1 = Graph('1', {node_trip1_o: 1, node_trip1_d: -1, node_trip2_o: 1, node_trip2_d: -1,
                          node_trip3_o: 1, node_trip3_d: -1, node_trip4_o: 1, node_trip4_d: -1,
                          node_pull_out_trip1: 0, node_pull_in_trip1: 0, node_pull_out_trip2: 0,
                          node_pull_in_trip2: 0, node_pull_out_trip3: 0, node_pull_in_trip3: 0,
                          node_pull_out_trip4: 0, node_pull_in_trip4: 0},
                    {arc_trip1: (1, 0), arc_trip2: (1, 0), arc_trip3: (1, 0), arc_trip4: (1, 0),
                     arc_pull_out_trip1: (1, 2), arc_pull_in_trip1: (1, 2), arc_pull_out_trip2: (1, 2),
                     arc_pull_in_trip2: (1, 2), arc_pull_out_trip3: (1, 2), arc_pull_in_trip3: (1, 2),
                     arc_pull_out_trip4: (1, 2), arc_pull_in_trip4: (1, 2),
                     arc_trip1d_trip3o: (1, 2), arc_trip2d_trip4o: (1, 2),
                     arc_trip1d_trip2o: (1, 2), arc_trip3d_trip4o: (1, 2),
                     arc_depot_standing1: (1, 2), arc_depot_standing2: (1, 2), arc_depot_standing3: (1, 2),
                     arc_depot_standing4: (1, 2), arc_depot_standing5: (1, 2), arc_depot_standing6: (1, 2),
                     arc_depot_standing7: (1, 2), arc_returning: (1, 2)})

    arc_depot_standingA = Arc(ArcType.STOPPED, node_pull_out_trip1, node_pull_in_trip1, 2)
    arc_depot_standingB = Arc(ArcType.STOPPED, node_pull_in_trip1, node_pull_out_trip3, 2)
    arc_depot_standingC = Arc(ArcType.STOPPED, node_pull_out_trip3, node_pull_in_trip3, 2)
    arc_depot_standingD = Arc(ArcType.STOPPED, node_pull_in_trip3, node_pull_out_trip4, 2)
    arc_depot_standingE = Arc(ArcType.STOPPED, node_pull_out_trip4, node_pull_in_trip4, 2)
    graph_2 = Graph('2', {node_trip1_o: 1, node_trip1_d: -1,
                          node_trip3_o: 1, node_trip3_d: -1, node_trip4_o: 1, node_trip4_d: -1,
                          node_pull_out_trip1: 0, node_pull_in_trip1: 0, node_pull_out_trip3: 0, node_pull_in_trip3: 0,
                          node_pull_out_trip4: 0, node_pull_in_trip4: 0},
                    {arc_trip1: (1, 0), arc_trip3: (1, 0), arc_trip4: (1, 0),
                     arc_pull_out_trip1: (1, 2), arc_pull_in_trip1: (1, 2), arc_pull_out_trip3: (1, 2),
                     arc_pull_in_trip3: (1, 2), arc_pull_out_trip4: (1, 2), arc_pull_in_trip4: (1, 2),
                     arc_trip1d_trip3o: (1, 2), arc_trip3d_trip4o: (1, 2),
                     arc_depot_standingA: (1, 2), arc_depot_standingB: (1, 2), arc_depot_standingC: (1, 2),
                     arc_depot_standingD: (1, 2), arc_depot_standingE: (1, 2), arc_returning: (1, 2)})

    princing = Pricing(graph_1.commodity_name)
    princing.build_network(graph_1)
    princing.execute()
    princing.print_solution()
    princing.plot_network()
