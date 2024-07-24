"""
    Task class containing max latency, needed frequency and data!
"""


def get_exec_time(size, needed_freq):
    return size / needed_freq


class Task:
    def __init__(self, power_needed, name, size, deadline, creator, creation_time, needed_freq=2):
        self.power_needed = power_needed
        self.name = name
        self.deadline = deadline
        self.exec_time = get_exec_time(size, needed_freq)
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