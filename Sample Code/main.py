from Topology import Topology
from UsersLayer import UsersLayer
from FogLayer import FogLayer
from CloudLayer import CloudLayer
from Node import Node, Layer
from Graph import MobilityGraph
from ZoneManager import ZoneBroadcaster
from Clock import Clock
from ZoneManager import ServiceZone
from Evaluater import Evaluator
from Config import Config

global user_layer, fog_layer, cloud_layer, zone_broadcaster, topology


def init_system():
    global user_layer, fog_layer, cloud_layer, zone_broadcaster, topology
    graph = MobilityGraph(xml_path="Sample Code/vehicles_data.xml")
    user_layer = UsersLayer(graph)
    fog_layer = FogLayer(graph)
    cloud_layer = CloudLayer()
    zone_broadcaster = ZoneBroadcaster()
    for i in range(Config.fog_node_count):
        fog_layer.add_node(
            Node(i, Layer.Fog, cpu_freq=2, x=i * 10, y=i * 10, coverage_radius=Config.fog_coverage_radius))
    cloud_layer.add_node(Node(0, Layer.Cloud, cpu_freq=2, x=0, y=0, coverage_radius=Config.cloud_coverage_radius))
    topology = Topology(user_layer, fog_layer, cloud_layer, graph)
    zones = []
    for i in range(Config.zone_count):
        zones.append(
            ServiceZone(x=i * 100 + 50, y=i * 100 + 50, coverage_radius=Config.zone_coverage_radius, name=f"Zone{i}")
        )
    zone_broadcaster.set_zones(zones)
    topology.set_zones(zones)
    for fog_node in fog_layer.get_nodes():
        topology.assign_fog_nodes_to_zones(fog_node)

    for zone in zones:
        print(
            f"{zone.name} x:{zone.x} y:{zone.y} coverage_radius:{zone.coverage_radius} covers nodes: {zone.fog_nodes}")


def step():
    for node in user_layer.get_nodes():
        task = node.generate_task(Clock.time)
        topology.assign_task(node, task, zone_broadcaster)

    topology.update_topology()
    log_current_state()


def log_current_state():
    for node in fog_layer.get_nodes():
        if len(node.tasks) > 0:
            print("Fog Node", node.id, "Tasks", len(node.tasks))
    for node in cloud_layer.get_nodes():
        if len(node.tasks) > 0:
            print("Cloud Node", node.id, "Tasks", len(node.tasks))
    print()


init_system()
for i in range(Config.simulation_duration):
    print("Iteration", i)
    step()

Evaluator.log_evaluation()
