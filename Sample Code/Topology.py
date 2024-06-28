from Node import Node
import Graph
from ZoneManager import *
from Node import Layer
from Clock import Clock
from Evaluater import Evaluater

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
        self.zones = []

    def set_zones(self, zone):
        self.zones = zone

    def update_topology(self):
        self.graph.update_graph()
        current_time = Clock.time
        migrations = self.check_migrations(current_time)
        for migration in migrations:
            print(f"Migration of task {migration.id} from {migration.creator.id} to {migration.destination.id}")
            Evaluater.migrations_count += 1

    def check_migrations(self, current_time):
        migrations = []
        for node in self.fog_layer.get_nodes():
            for task in node.get_ongoing_tasks(current_time):
                if not node.is_in_range(task.creator.x, task.creator.y):
                    migrations.append(task)
        return migrations

    def assign_fog_nodes_to_zones(self, fog_node):
        for zone in self.zones:
            if zone.is_within_coverage(fog_node.x, fog_node.y):
                zone.add_fog_node(fog_node)

    def assign_task(self, user_node, task, zone_broadcast: ZoneBroadcaster):
        offers = zone_broadcast.broadcast(user_node, task)

        is_successful = False
        while not is_successful and len(offers) > 0:
            min_distance = float('inf')
            best_zone = None
            for offer in offers:
                zone_name, fog_node = offer
                zone = zone_broadcast.get_zone(zone_name)
                distance = fog_node.distance(user_node)
                if distance < min_distance:
                    min_distance = distance
                    best_zone = zone
            # accept offer
            is_successful = best_zone.accept_offer(user_node, task)
            if not is_successful:
                offers.remove((best_zone.name, best_zone.assignee))

        if len(offers) == 0:
            assignee = self.cloud_layer.get_nodes()[0]
            assignee.append_task(task)
