"""
    Class representing the Fog Layer!
"""
from Node import Layer

class FogLayer:
    def __init__(self) -> None:
        self.nodes = []

    def has_node(self, node):
        return node in self.nodes

    def add_node(self, node):
        node.layer = Layer.Fog
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes