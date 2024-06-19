
"""
    Node class representing any computational power from any layer! Adjust the cpu_freq and the layer
    properly!
"""

class Node:
    def __init__(self, id, layer):
        self.id = id
        self.layer = layer
        self.cpu_freq = 2
