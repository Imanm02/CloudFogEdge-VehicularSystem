"""
    Class representing the Mobility Graph! This Graph should update the dictionary based on the
    info from the sumo xml parser!
"""
from SumoXMLParser import SumoXMLParser


class MobilityGraph:
    def __init__(self, xml_path) -> None:
        self.nodes = []
        self.graph = {}
        self.xml_path = xml_path
        self.current_time = 0
        self.init_graph()

    def init_graph(self):
        parser = SumoXMLParser(filepath="fcd_output.xml")
        self.graph = parser.parse()
        self.current_time = min(self.graph.keys())
        self.nodes = self.graph[self.current_time]

    def update_graph(self):
        self.current_time += 1
        if self.current_time in self.graph:
            self.nodes = self.graph[self.current_time]
        else:
            self.nodes = []
        return self.nodes

    def get_nodes(self):
        return self.nodes

    def get_current_time(self):
        return self.current_time