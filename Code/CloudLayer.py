
""" 
    Class representing the Cloud Layer! It contains a list Nodes
    in most cases it should contain 1 node.
"""
from Node import Layer

class CloudLayer:
    def __init__(self) -> None:
        self.nodes = []

    def add_node(self, node):
        node.layer = Layer.Cloud
        self.nodes.append(node)

    def get_nodes(self):
        return self.nodes
