

"""
    Class representing the Fog Layer!
"""

class FogLayer:
    def __init__(self) -> None:
        self.nodes = []

    def has_node(self, node):
        return node in self.nodes