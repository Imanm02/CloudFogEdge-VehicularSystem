"""
    Node class representing any computational power from any layer! Adjust the cpu_freq and the layer
    properly!
"""
import math


class Layer:
    Users = 0
    Fog = 1
    Cloud = 2


class Node:
    def __init__(self, id, layer, cpu_freq=2, x=0, y=0, coverage_radius=0):
        self.id = id
        self.layer = layer
        self.cpu_freq = cpu_freq
        self.x = x
        self.y = y
        self.coverage_radius = coverage_radius
        self.tasks = []

    def distance(self, node):
        return math.sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)

    def append_task(self, task):
        self.tasks.append(task)