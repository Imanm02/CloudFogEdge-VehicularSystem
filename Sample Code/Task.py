"""
    Task class containing max latency, needed frequency and data!
"""


# def get_needed_freq(cpu_cycles, deadline):
#     return cpu_cycles / deadline


class Task:
    def __init__(self, power_needed, name, size, deadline, creator, creation_time):
        self.power_needed = power_needed
        self.name = name
        self.deadline = deadline * 2
        self.exec_time = deadline
        self.size = size
        self.creation_time = creation_time
        self.creator = creator
        self.assigned_node = None
        self.result = None
        self.time_taken = deadline - creation_time

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result

    def set_assignee(self, node):
        self.assigned_node = node

# class TaskProfile:
#     #todo implement
