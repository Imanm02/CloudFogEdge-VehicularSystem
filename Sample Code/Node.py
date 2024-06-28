"""
    Node class representing any computational power from any layer! Adjust the cpu_freq and the layer
    properly!
"""
import math
import random
from Task import Task
from Clock import Clock
from Evaluater import Evaluator
from ZoneManager import ServiceZone


class Layer:
    Users = 0
    Fog = 1
    Cloud = 2


class Node:
    def __init__(self, id, layer, cpu_freq=2, x=0, y=0, coverage_radius=0, speed=0, angle=-1):
        self.id = id
        self.layer = layer
        self.cpu_freq = cpu_freq
        self.x = x
        self.y = y
        self.coverage_radius = coverage_radius
        self.angle = angle
        self.tasks = []

    def __repr__(self):
        return f"Node(id={self.id}, x={self.x}, y={self.y})"

    def distance(self, node):
        return math.sqrt((self.x - node.x) ** 2 + (self.y - node.y) ** 2)

    def append_task(self, task):
        self.tasks.append(task)

    def generate_task(self, creation_time):
        task = Task(
            name="T" + str(random.randint(1, 100)),
            cpu_cycles=random.randint(1, 10),
            size=random.randint(1, 10),
            deadline=random.randint(1, 10),
            creator=self,
            creation_time=creation_time
        )
        Evaluator.total_tasks += 1
        return task

    def get_ongoing_tasks(self, current_time):
        output = []
        for task in self.tasks:
            if task.creation_time + task.deadline <= current_time and task.assigned_node == self:
                output.append(task)
        return output

    def is_free(self, current_time):
        return len(self.get_ongoing_tasks(current_time)) == 0

    def is_in_range(self, x, y):
        return self.distance(Node(-1, Layer.Users, x, y)) <= self.coverage_radius

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

