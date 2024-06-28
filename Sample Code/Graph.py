"""
    Class representing the Mobility Graph! This Graph should update the dictionary based on the
    info from the sumo xml parser!
"""
from SumoXMLParser import SumoXMLParser
from Clock import Clock


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
            self.nodes = self.graph[Clock.time]
        else:
            self.nodes = []
        return self.nodes

    def get_nodes(self):
        return self.nodes

    def get_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None
