"""
    Node class representing any computational power from any layer! Adjust the cpu_freq and the layer
    properly!
"""
import math
import random
from Task import Task
from Clock import Clock
from Evaluater import Evaluator
from Config import Config


class Layer:
    Users = 0
    Fog = 1
    Cloud = 2


class Node:
    def __init__(self, id, layer, power=Config.FOG_POWER, x=0, y=0, coverage_radius=0, speed=0, angle=-1):
        self.id = id
        self.layer = layer
        self.power = power
        self.x = x
        self.y = y
        self.speed = speed
        self.coverage_radius = coverage_radius
        self.angle = angle
        self.tasks = []

    def __repr__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y})"

    def distance(self, node):
        return math.sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)

    def append_task(self, task):
        self.tasks.append(task)
        self.power -= task.power_needed

    def generate_task(self, task_data):
        task = Task(
            name=task_data['name'],
            power_needed=task_data['power_needed'],
            size=task_data['size'],
            deadline=task_data['deadline'],
            creator=self,
            creation_time=task_data['creation_time']
        )
        Evaluator.total_tasks += 1
        return task

    def is_in_range(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2) <= self.coverage_radius

    def deliver_task_result(self, task):
        task.assigned_node = None
        if Clock.time - task.creation_time <= task.deadline:
            print(f"Task {task.name} is done and delivered on time!")
        else:
            print(f"Task {task.name} is done but delivered late!")
            Evaluator.deadline_misses += 1

    def is_done(self, task):
        if Clock.time - task.creation_time >= task.deadline:
            task.set_result("Random Result")
            return True
        return False

    def remove_task(self, task):
        self.tasks.remove(task)
        self.power += task.power_needed
