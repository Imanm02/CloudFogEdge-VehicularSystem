from Node import Node
import Graph
from Node import Layer

"""
    Topology class containing the three layers! The main algorithm should be implemented as a method of 
    this class!
"""


class Topology:
    def __init__(self, user_layer, fog_layer, cloud_layer, graph, timeslot_length=1):
        self.user_layer = user_layer
        self.fog_layer = fog_layer
        self.cloud_layer = cloud_layer
        self.graph = graph
        self.TIMESLOT_LENGTH = timeslot_length

    def update_topology(self):
        self.graph.update_graph()

    def assign_task(self, user_node, task):
        assignee = self.find_assignee(user_node, task)
        task.set_assignee(assignee)
        assignee.append_task(task)

    def find_assignee(self, user_node, task):
        # todo complete the algorithm. its so simple now that it just assigns the task to the first node in range
        #  that is not busy
        current_time = self.graph.get_current_time()
        x, y = user_node.x, user_node.y

        for node in self.fog_layer.get_nodes():
            if node.cpu_freq >= task.needed_freq and node.is_in_range(x, y) and node.is_free(current_time):
                return node
        for node in self.cloud_layer.get_nodes():
            return node
