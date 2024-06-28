import math
from Node import Node
from Clock import Clock


class ServiceZone:
    def __init__(self, x, y, coverage_radius, name):
        """
        x: x-coordinate of the base station
        y: y-coordinate of the base station
        coverage_radius: radius of the coverage circle in meters
        """
        self.x = x
        self.y = y
        self.coverage_radius = coverage_radius
        self.name = name
        self.fog_nodes = []

    def is_within_coverage(self, point_x, point_y):
        """
        Checks if a given point is within the coverage radius of the base station.
        point_x: x-coordinate of the point to check
        point_y: y-coordinate of the point to check
        """
        distance = math.sqrt((point_x - self.x) ** 2 + (point_y - self.y) ** 2)
        return distance <= self.coverage_radius

    def add_fog_node(self, fog_node):
        self.fog_nodes.append(fog_node)

    def find_assignee(self, user_node, task):
        # todo complete the algorithm. its so simple now (greedy)
        current_time = Clock.time
        x, y = user_node.x, user_node.y

        min_distance = float('inf')
        assignee = None
        for node in self.fog_nodes:
            if node.cpu_freq >= task.needed_freq and node.is_in_range(x, y) and node.is_free(current_time):
                distance = node.distance(user_node)
                if distance < min_distance:
                    min_distance = distance
                    assignee = node
        return assignee

    def create_offer(self, node, task):
        if not self.is_within_coverage(node.x, node.y):
            return None
        fog = self.find_assignee(node, task)
        if fog is None:
            return None
        offer = (self.name, fog)
        return offer

    def accept_offer(self, user_node, task):
        assignee = self.find_assignee(user_node, task)
        if assignee is not None:
            assignee.append_task(task)
            return True
        return False


class ZoneBroadcaster:
    def __init__(self):
        self.zones = []

    def add_zone(self, name, x, y, coverage_radius):
        zone = ServiceZone(x, y, coverage_radius, name)
        self.zones.append(zone)

    def get_nearest_zone(self, x, y):
        nearest_zone = None
        min_distance = float('inf')
        for zone in self.zones:
            distance = math.sqrt((x - zone.x) ** 2 + (y - zone.y) ** 2)
            if distance < min_distance:
                min_distance = distance
                nearest_zone = zone
        return nearest_zone

    def broadcast(self, user, task):
        offers = []
        for zone in self.zones:
            offer = zone.create_offer(user, task)
            if offer:
                offers.append(offer)
        return offers

    def get_zone(self, zone_name):
        for zone in self.zones:
            if zone.name == zone_name:
                return zone
        return None
