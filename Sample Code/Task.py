"""
    Task class containing max latency, needed frequency and data!
"""

def get_needed_freq(cpu_cycles, deadline):
    return cpu_cycles / deadline


class Task:
    def __init__(self, cpu_cycles, name, size, deadline, creator, creation_time):
        self.cpu_cycles = cpu_cycles
        self.name = name
        self.deadline = deadline
        self.size = size
        self.creation_time = creation_time
        self.needed_freq = get_needed_freq(cpu_cycles, deadline)
        self.creator = creator
        self.assigned_node = None
        self.result = None

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result

    def set_assignee(self, node):
        self.assigned_node = node


# class TaskProfile:
#     #todo implement
