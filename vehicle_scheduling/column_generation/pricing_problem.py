import networkx as nx
import matplotlib.pyplot as plt

from vehicle_scheduling.graph.graph import Graph


class Subproblem:

    def __init__(self, garage_name):
        self.network = nx.DiGraph(name=garage_name)

    def build_network(self, graph: Graph):
        for node in graph.nodes:
            self.network.add_node(node, demand=node.demand, pos=(node.time*1000, node.position_station_representation))
        for arc in graph.arcs:
            self.network.add_edge(arc.origin_node, arc.destination_node, weight=arc.cost,
                                  capacity=arc.capacity, original_events=arc, color='black')
            self.network.edges
        self.network.edges

    def update_arc_costs(self, trips_arcs_reduced_costs: dict):
        for trip_arc in trips_arcs_reduced_costs.items():
            self.network[trip_arc[0][0]][trip_arc[0][1]]['cost'] = trip_arc[1]
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
        for node_origen in solution.keys():
            for node_destination in solution[node_origen].keys():
                print(node_origen, node_destination, "|",
                      self.network[node_origen][node_destination]['original_events'], "|",
                      solution[node_origen][node_destination])
        print("------------")

    def get_solution(self):
        solution = nx.min_cost_flow(self.network)
        for node_origen in solution.keys():
            for node_destination in solution[node_origen].keys():
                if solution[node_origen][node_destination] > 0 or self.network[node_origen][node_destination]['capacity'] == 0:
                    print(node_origen, node_destination, "|",
                          self.network[node_origen][node_destination]['original_events'], "|",
                          solution[node_origen][node_destination])
                    self.network[node_origen][node_destination]['color'] = 'red' if solution[node_origen][node_destination] > 0 else 'green'

    def plot_network(self):
        edge_labels = {}
        pos = nx.get_node_attributes(self.network, 'pos')
        color_edges = [self.network[u][v]['color'] for u, v in self.network.edges]
        nx.draw(self.network, pos, edges=self.network.edges, edge_color=color_edges, with_labels=True, node_size=50, alpha=0.7, arrows=True, font_size=8, arrowsize=11)
        labels_return = nx.draw_networkx_edge_labels(self.network, pos, edge_labels=edge_labels, font_size=9)
        plt.show()
