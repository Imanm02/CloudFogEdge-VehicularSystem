"""
    Class representing the Mobility Graph! This Graph should update the dictionary based on the
    info from the sumo xml parser!
"""
from SumoXMLParser import SumoXMLParser
from Clock import Clock
from Node import Layer


class MobilityGraph:
    def __init__(self, xml_path) -> None:
        self.nodes = []
        self.graph = {}
        self.xml_path = xml_path
        self.init_graph()

    def init_graph(self):
        parser = SumoXMLParser(filepath=self.xml_path)
        self.graph = parser.parse()
        Clock.time = min(self.graph.keys())
        self.nodes = self.graph[Clock.time]

    def update_graph(self):
        Clock.time += 1
        if Clock.time in self.graph:
            new_nodes = self.graph[Clock.time]
            for node in self.nodes:
                new_node = next((n for n in new_nodes if n.id == node.id), None)
                if new_node is not None:
                    node.x = new_node.x
                    node.y = new_node.y
            self.nodes = new_nodes
        else:
            self.nodes = []
        return self.nodes

    def get_user_nodes(self):
        return [node for node in self.nodes if node.layer == Layer.Users]

    def get_moving_fog_nodes(self):
        return [node for node in self.nodes if node.layer == Layer.Fog]

    def get_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None
