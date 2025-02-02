from Node import Layer

"""
    Class representing the Users layer!
"""

from Graph import MobilityGraph

class UsersLayer:
    def __init__(self, graph) -> None:
        self.graph = graph

    def get_nodes(self):
        return self.graph.get_user_nodes()

    def get_nodes_by_id(self, id):
        return self.graph.get_node(id)