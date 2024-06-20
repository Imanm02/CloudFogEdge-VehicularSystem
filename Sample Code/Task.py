
"""
    Task class containing max latency, needed frequency and data!
"""

class Task:
    def __init__(self, needed_freq, max_time, data, deadline):
        self.needed_freq = needed_freq
        self.max_time = max_time
        self.data = data
        self.deadline = deadline
        self.assigned_node = None