"""
    Class for parsing the .xml file output of the SUMO simulator!
"""
import xml.etree.ElementTree as ET
import Node
from Config import Config


class SumoXMLParser:
    def __init__(self, file_path, mobile_file_path):
        self.filepath = file_path
        self.mobileFilepath = mobile_file_path

    def parse(self):
        tree = ET.parse(self.filepath)
        root = tree.getroot()
        # vehicles is a mapping from time to a list of vehicles
        vehicles = {}
        self.getVehicles(root, vehicles)

        tree = ET.parse(self.mobileFilepath)
        root = tree.getroot()
        self.getVehicles(root, vehicles)
        return vehicles

    def getVehicles(self, root, vehicles):
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
                        coverage_radius=Config.FOG_COVERAGE_RADIUS
                    ))
