"""
    Class representing the Mobility Graph! This Graph should update the dictionary based on the
    info from the sumo xml parser!
"""
from SumoXMLParser import SumoXMLParser
from Clock import Clock
from Node import Layer


class MobilityGraph:
    def __init__(self, xml_path, mobile_xml_path, task_file_path, fixed_fog_node_file_path, zone_file_path) -> None:
        self.nodes = []
        self.graph = {}
        self.xml_path = xml_path
        self.mobile_xml_path = mobile_xml_path
        self.task_file_path = task_file_path
        self.fixed_fog_node_file_path = fixed_fog_node_file_path
        self.zone_file_path = zone_file_path
        self.init_graph()

    def init_graph(self):
        parser = SumoXMLParser(file_path=self.xml_path, mobile_file_path=self.mobile_xml_path,
                               task_file_path=self.task_file_path,
                               fixed_fog_node_file_path=self.fixed_fog_node_file_path,
                               zone_file_path=self.zone_file_path)
        self.graph = parser.parse()
        Clock.time = min(self.graph.keys())
        self.nodes = self.graph[Clock.time]

    def update_graph(self):
        Clock.time += 1
        new_nodes = self.graph[Clock.time]
        for node in self.nodes:
            new_node = next((n for n in new_nodes if n.id == node.id), None)
            if new_node is not None:
                node.x = new_node.x
                node.y = new_node.y
                node.angle = new_node.angle
                node.speed = new_node.speed
        return self.nodes

    def get_tasks(self):
        parser = SumoXMLParser(file_path=self.xml_path, mobile_file_path=self.mobile_xml_path,
                               task_file_path=self.task_file_path,
                               fixed_fog_node_file_path=self.fixed_fog_node_file_path,
                               zone_file_path=self.zone_file_path)
        return parser.parse_task()

    def get_fixed_fog_node(self):
        parser = SumoXMLParser(file_path=self.xml_path, mobile_file_path=self.mobile_xml_path,
                               task_file_path=self.task_file_path,
                               fixed_fog_node_file_path=self.fixed_fog_node_file_path,
                               zone_file_path=self.zone_file_path)
        return parser.parse_fixed_fog_node()

    def get_zones(self):
        parser = SumoXMLParser(file_path=self.xml_path, mobile_file_path=self.mobile_xml_path,
                               task_file_path=self.task_file_path,
                               fixed_fog_node_file_path=self.fixed_fog_node_file_path,
                               zone_file_path=self.zone_file_path)
        return parser.parse_zone()

    def get_user_nodes(self):
        return [node for node in self.nodes if node.layer == Layer.Users]

    def get_moving_fog_nodes(self):
        return [node for node in self.nodes if node.layer == Layer.Fog]

    def get_node(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None
