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

global user_layer, fog_layer, cloud_layer, zone_broadcaster, topology, task_data


# graph = MobilityGraph(xml_path="./vehicles_data.xml", mobile_xml_path="./mobileFogNodes_data.xml",
#                       task_file_path="./tasks_data.xml", fixed_fog_node_file_path="./fixedFogNodes_data.xml")
def init_system():
    global user_layer, fog_layer, cloud_layer, zone_broadcaster, topology, task_data
    graph = MobilityGraph(xml_path="./vehicles_data.xml", mobile_xml_path="./mobileFogNodes_data.xml",
                          task_file_path="./tasks_data.xml", fixed_fog_node_file_path="./fixedFogNodes_data.xml",
                          zone_file_path="./zones_data.xml")
    task_data = graph.get_tasks()
    user_layer = UsersLayer(graph)
    fog_layer = FogLayer(graph)
    cloud_layer = CloudLayer()
    zone_broadcaster = ZoneBroadcaster()
    for fixed_fog_node in graph.get_fixed_fog_node():
        fog_layer.add_node(fixed_fog_node)
    cloud_layer.add_node(Node(0, Layer.Cloud, cpu_freq=2, x=0, y=0, coverage_radius=Config.CLOUD_COVERAGE_RADIUS))
    topology = Topology(user_layer, fog_layer, cloud_layer, graph)
    zones = []
    for zone in graph.get_zones():
        zones.append(zone)
    zone_broadcaster.set_zones(zones)
    topology.set_zones(zones)
    for fog_node in fog_layer.get_nodes():
        topology.assign_fog_nodes_to_zones(fog_node)

    for zone in zones:
        print(
            f"{zone.name} x:{zone.x} y:{zone.y} coverage_radius:{zone.coverage_radius} covers nodes: {zone.fog_nodes}")


def step():
    global task_data
    for i in task_data:
        if i["creation_time"] == Clock.time:
            node: Node = user_layer.get_nodes_by_id(i["creator"])
            task = node.generate_task(i)
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
for i in range(Config.SIMULATION_DURATION):
    print("Iteration", i)
    step()

Evaluator.log_evaluation()
