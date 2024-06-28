"""
    Class representing the Fog Layer!
"""
from Node import Layer


class FogLayer:
    def __init__(self, graph) -> None:
        self.graph = graph
        self.nodes = self.graph.get_moving_fog_nodes()

    def add_node(self, node):
        node.layer = Layer.Fog
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes
