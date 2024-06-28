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
        current_time = self.graph.get_current_time()
        migrations = self.check_migrations(current_time)
        for task in migrations:
            # todo complete it!
            pass

    def check_migrations(self, current_time):
        migrations = []
        for node in self.fog_layer.get_nodes():
            for task in node.get_ongoing_tasks(current_time):
                if not node.is_in_range(task.creator.x, task.creator.y):
                    migrations.append(task)
        return migrations

    def assign_task(self, user_node, task, fog_nodes):

        assignee = self.find_assignee(user_node, task, fog_nodes)
        task.set_assignee(assignee)
        assignee.append_task(task)

    def find_assignee(self, user_node, task, fog_nodes):
        # todo complete the algorithm. its so simple now (greedy)
        current_time = self.graph.get_current_time()
        x, y = user_node.x, user_node.y

        min_distance = float('inf')
        assignee = None
        for node in fog_nodes:
            if node.cpu_freq >= task.needed_freq and node.is_in_range(x, y) and node.is_free(current_time):
                distance = node.distance(user_node)
                if distance < min_distance:
                    min_distance = distance
                    assignee = node
        if assignee is None:
            assignee = self.cloud_layer.get_nodes()[0]
        return assignee
