"""
    Task class containing max latency, needed frequency and data!
"""


def get_needed_freq(cpu_cycles, deadline):
    return cpu_cycles / deadline


class Task:
    def __init__(self, cpu_cycles, name, size, deadline, owner_node, creation_time):
        self.cpu_cycles = cpu_cycles
        self.name = name
        self.deadline = deadline
        self.size = size
        self.creation_time = creation_time
        self.needed_freq = get_needed_freq(cpu_cycles, deadline)
        self.owner_node = owner_node
        self.assigned_node = None

    def set_assignee(self, node):
        self.assigned_node = node
