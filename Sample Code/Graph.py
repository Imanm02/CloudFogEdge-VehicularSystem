
"""
    Class representing the Mobility Graph! This Graph should update the dictionary based on the
    info from the sumo xml parser!
"""

class MobilityGraph:
    def __init__(self) -> None:
        self.nodes = []
        self.graph = {}


    def add_node(self, node):
        self.nodes.append(node)
        self.graph[node] = []

    def add_edge(self, node1, node2, weight):
        self.graph[node1].append((node2, weight))
        self.graph[node2].append((node1, weight))

    def get_nearest_node(self, node, layer):
        nearest_node = None
        min_distance = float('inf')
        for n in self.nodes:
            if n.layer == layer:
                distance = node.distance(n)
                if distance < min_distance:
                    min_distance = distance
                    nearest_node = n
        return nearest_node

    def get_edge_weight(self, node1, node2):
        for n, w in self.graph[node1]:
            if n == node2:
                return w
        return None