from ZoneManager import *

"""
    Topology class containing the three layers! The main algorithm should be implemented as a method of 
    this class!
"""

from Node import Node


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
        for zone_manager in self.zones:
            zone_manager.update(self)

    def assign_fog_nodes_to_zones(self, fog_node):
        for zone in self.zones:
            if zone.is_within_coverage(fog_node.x, fog_node.y):
                zone.add_fog_node(fog_node)

    def assign_task(self, user_node: Node, task, zone_broadcast: ZoneBroadcaster):
        new_x = user_node.x + user_node.speed * self.TIMESLOT_LENGTH * math.cos(user_node.angle)
        new_y = user_node.y + user_node.speed * self.TIMESLOT_LENGTH * math.sin(user_node.angle)
        current_zones = zone_broadcast.get_zones_by_position(user_node.x, user_node.y)
        predicted_zones = zone_broadcast.get_zones_by_position(new_x, new_y)

        if predicted_zones:
            target_zones = predicted_zones
        else:
            target_zones = current_zones
        offers = zone_broadcast.broadcast_to_zones(target_zones, user_node, task)

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

    def get_node(self, node_id):
        return self.graph.get_node(node_id)

    def get_nearest_zone(self, x, y):
        nearest_zone = None
        min_distance = float('inf')
        for zone in self.zones:
            distance = math.sqrt((x - zone.x) ** 2 + (y - zone.y) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_zone = zone
        return nearest_zone
