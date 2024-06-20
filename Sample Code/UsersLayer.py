from Node import Layer


"""
    Class representing the Users layer!
"""
class UsersLayer:
    def __init__(self) -> None:
        self.nodes = []

    def has_node(self, node):
        return node in self.nodes

    def add_node(self, node):
        node.layer = Layer.Users
        self.nodes.append(node)