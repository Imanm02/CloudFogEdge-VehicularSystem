from Node import Node
from Graph import Graph
from FogLayer import FogLayer

"""
    Topology class containing the three layers! The main algorithm should be implemented as a method of 
    this class!
"""

class Topology:
    def __init__(self, timeslot_length = 1) -> None:
        self.user_layer = None
        self.fog_layer = None
        self.cloud_layer = None
        self.graph = None
        self.TIMESLOT_LENGTH = timeslot_length


   

