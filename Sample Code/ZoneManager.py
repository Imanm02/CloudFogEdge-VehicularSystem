import math

from Config import Config

from Clock import Clock
from Task import Task
from Evaluater import Evaluator
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

    def find_assignee(self, user_node, task):
        # todo complete the algorithm. its so simple now (greedy)
        x, y = user_node.x, user_node.y

        x = user_node.x + user_node.speed * 1 * math.cos(user_node.angle)
        y = user_node.y + user_node.speed * 1 * math.sin(user_node.angle)
        min_distance = float('inf')
        assignee = None
        for node in self.fog_nodes:
            if node.cpu_freq >= task.needed_freq and node.is_in_range(x, y):
                distance = node.distance(user_node)
                if self.enough_time(task, distance):
                    continue
                if distance < min_distance:
                    min_distance = distance
                    assignee = node
        return assignee

    def enough_time(self, task, distance):
        time = Config.PACKET_COST_PER_METER * distance * 4 + Config.TASK_COST_PER_METER * distance * 2
        return task.time_taken < time

    def create_offer(self, node, task):
        if not self.is_within_coverage(node.x, node.y):
            return None
        fog = self.find_assignee(node, task)
        if fog is None:
            return None
        offer = (self.name, fog)
        return offer

    def accept_offer(self, user_node, task):
        assignee: Node = self.find_assignee(user_node, task)
        if assignee is not None:
            assignee.append_task(task)
            assignee.cpu_freq -= task.needed_freq
            return True
        return False

    def update(self, topology):
        for fog_node in self.fog_nodes:
            for task in fog_node.tasks:
                if fog_node.is_done(task):
                    fog_node.remove_task(task)
                    fog_node.cpu_freq += task.needed_freq
                    creator = topology.get_node(task.creator.id)
                    nearest_zone = topology.get_nearest_zone(creator.x, creator.y)
                    if nearest_zone == self:
                        self.send_task_result_to_owner(task, topology)
                    else:
                        Evaluator.migrations_count += 1
                        print(
                            f"The result of task {task.name} is sent to zone {nearest_zone.name} from zone {self.name}")
                        nearest_zone.send_task_result_to_owner(task, topology)

        for fog_node in self.fog_nodes:
            if not self.is_within_coverage(fog_node.x, fog_node.y):
                self.fog_nodes.remove(fog_node)
                topology.assign_fog_nodes_to_zones(fog_node)
                print(f"The moving fog node {fog_node.id} is now out of zone {self.name}")

    def send_task_result_to_owner(self, task: Task, topology):
        owner_id = task.creator.id
        owner = topology.get_node(owner_id)
        x, y = owner.x, owner.y
        owner.deliver_task_result(task)
        print(f"Task {task.name} is sent to owner {owner_id} at ({x}, {y})")


class ZoneBroadcaster:
    def __init__(self):
        self.zones = []

    def set_zones(self, zones):
        self.zones = zones

    def get_zone(self, zone_name):
        for zone in self.zones:
            if zone.name == zone_name:
                return zone
        return None

    def get_zones_by_position(self, x, y):
        possible_zones = []
        for zone in self.zones:
            if zone.is_within_coverage(x, y):
                possible_zones.append(zone)
        return possible_zones

    def broadcast_to_zones(self, zones, user_node, task):

        offers = []
        for zone in zones:
            offer = zone.create_offer(user_node, task)
            if offer:
                offers.append(offer)
        return offers
