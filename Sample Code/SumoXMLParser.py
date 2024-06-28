"""
    Class for parsing the .xml file output of the SUMO simulator!
"""
import xml.etree.ElementTree as ET
import Node
from Config import Config


class SumoXMLParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        # vehicles is a mapping from time to a list of vehicles
        vehicles = {}
        for timestep in root.findall('timestep'):
            time = float(timestep.get('time'))
            for vehicle in timestep.findall('vehicle'):
                vehicle_id = vehicle.get('id')
                x = float(vehicle.get('x'))
                y = float(vehicle.get('y'))
                speed = float(vehicle.get('speed'))
                angle = float(vehicle.get('angle'))
                if time not in vehicles:
                    vehicles[time] = []
                type = vehicle.get('type')
                if type == 'moblieFog':
                    vehicles[time].append(Node.Node(vehicle_id, Node.Layer.Fog, x=x, y=y, speed=speed, angle=angle))
                else:
                    vehicles[time].append(Node.Node(
                        id=vehicle_id,
                        layer=Node.Layer.Users,
                        x=x,
                        y=y,
                        speed=speed,
                        angle=angle,
                        coverage_radius=Config.fog_coverage_radius
                    ))
        return vehicles
