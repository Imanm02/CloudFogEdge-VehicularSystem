"""
    Class for parsing the .xml file output of the SUMO simulator!
"""
import xml.etree.ElementTree as ET
import Node
from Config import Config
from Task import Task
from ZoneManager import ServiceZone


class SumoXMLParser:
    def __init__(self, file_path, mobile_file_path, task_file_path, fixed_fog_node_file_path, zone_file_path):
        self.filepath = file_path
        self.mobileFilepath = mobile_file_path
        self.taskFilePath = task_file_path
        self.zoneFilePath = zone_file_path
        self.fixedFogNodeFilePath = fixed_fog_node_file_path

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
                if type == 'mobileFog':
                    vehicles[time].append(Node.Node(vehicle_id, Node.Layer.Fog, x=x, y=y, speed=speed, angle=angle,
                                                    coverage_radius=Config.FOG_COVERAGE_RADIUS))
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

    def parse_task(self):
        tree = ET.parse(self.taskFilePath)
        root = tree.getroot()
        task_data = []
        for task in root.findall('task'):
            name = task.get('name')
            creation_time = float(task.get('creation_time'))
            deadline = float(task.get('deadline'))
            cpu_cycles = float(task.get('power_needed'))
            size = float(task.get('size'))
            creator = task.get('creator')
            task_data.append({"name": name,
                              "cpu_cycles": cpu_cycles,
                              "size": size,
                              "deadline": deadline,
                              "creator": creator,
                              "creation_time": creation_time})

        return task_data

    def parse_fixed_fog_node(self):
        tree = ET.parse(self.fixedFogNodeFilePath)
        root = tree.getroot()
        nodes = []
        for task in root.findall('node'):
            id = task.get('id')
            x = float(task.get('x'))
            y = float(task.get('y'))
            type = task.get('type')
            power = float(task.get('power'))
            lane = int(task.get('lane'))
            nodes.append(
                Node.Node(id, Node.Layer.Fog, cpu_freq=power, x=x, y=y, coverage_radius=Config.FOG_COVERAGE_RADIUS))
        return nodes

    def parse_zone(self):
        tree = ET.parse(self.zoneFilePath)
        root = tree.getroot()
        zones = []
        for task in root.findall('zone'):
            name = task.get('name')
            x = float(task.get('x'))
            y = float(task.get('y'))
            coverage_radius = float(task.get('coverage_radius'))
            zones.append(
                ServiceZone(x=x, y=y, coverage_radius=coverage_radius,
                            name=name))
        return zones
