from Node import Node
import Graph
from Node import Layer

"""
    Topology class containing the three layers! The main algorithm should be implemented as a method of 
    this class!
"""

class Topology:
    def __init__(self, timeslot_length = 1) -> None:
        self.user_layer = None
        self.fog_layer = None
        self.cloud_layer = None
        self.graph = None
        self.TIMESLOT_LENGTH = timeslot_length

    def add_user(self, user):
        self.user_layer.add_node(user)

    def add_fog_node(self, node):
        self.fog_layer.add_node(node)

    def add_cloud_node(self, node):
        self.cloud_layer.add_node(node)

    def add_edge(self, node1, node2, weight):
        self.graph.add_edge(node1, node2, weight)

    def find_assignee(self, user_node, task):
        fog_node = self.graph.get_nearest_node(user_node, Layer.Fog)
        cloud_node = self.graph.get_nearest_node(fog_node, Layer.Cloud)
        fog_distance = self.graph.get_edge_weight(user_node, fog_node)
        cloud_distance = self.graph.get_edge_weight(fog_node, cloud_node)

        task_user_time = task.cpu_cycles / user_node.cpu_freq
        task_fog_time = task.cpu_cycles / fog_node.cpu_freq + task.data / fog_distance
        task_cloud_time = task.cpu_cycles / cloud_node.cpu_freq + task.data / cloud_distance

        if task_user_time < task_fog_time and task_user_time < task_cloud_time:
            return user_node
        elif task_fog_time < task_user_time and task_fog_time < task_cloud_time:
            return fog_node
        else:
            return cloud_node

    def assign_task(self, user_node, task):
        assignee = self.find_assignee(user_node, task)
        task.assigned_node = assignee
        assignee.append_task(task)