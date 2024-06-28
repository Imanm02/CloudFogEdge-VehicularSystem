import math
from Node import Node


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
        nearest_zone: ServiceZone = self.get_nearest_zone(user.x, user.y)

        if nearest_zone:
            return nearest_zone
        else:
            print(f"No zone available near the position ({user.x}, {user.y})")
            return None
