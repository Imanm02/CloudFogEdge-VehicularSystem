import math

class ServiceZone:
    def __init__(self, x, y, coverage_radius):
        """
        x: x-coordinate of the base station
        y: y-coordinate of the base station
        coverage_radius: radius of the coverage circle in meters
        """
        self.x = x
        self.y = y
        self.coverage_radius = coverage_radius

    def is_within_coverage(self, point_x, point_y):
        """
        Checks if a given point is within the coverage radius of the base station.
        point_x: x-coordinate of the point to check
        point_y: y-coordinate of the point to check
        """
        distance = math.sqrt((point_x - self.x) ** 2 + (point_y - self.y) ** 2)
        return distance <= self.coverage_radius


