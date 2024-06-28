from Topology import Topology
from UsersLayer import UsersLayer
from FogLayer import FogLayer
from CloudLayer import CloudLayer
from Node import Node, Layer
from Graph import MobilityGraph
from ZoneManager import ZoneBroadcaster
from Clock import Clock

fog_layer = FogLayer()
for i in range(100):
    fog_layer.add_node(Node(i, Layer.Fog, cpu_freq=2, x=i * 10, y=i * 10, coverage_radius=100))

cloud_layer = CloudLayer()
cloud_layer.add_node(Node(0, Layer.Cloud, cpu_freq=2, x=0, y=0, coverage_radius=1000))

graph = MobilityGraph(xml_path="./fcd_output.xml")
user_layer = UsersLayer(graph)

topology = Topology(user_layer, fog_layer, cloud_layer, graph)

zone_broadcaster = ZoneBroadcaster()
for i in range(10):
    zone_broadcaster.add_zone(f"Zone{i}", x=i * 100 + 50, y=i * 100 + 50, coverage_radius=200)
topology.set_zones(zone_broadcaster.zones)

for fog_node in fog_layer.get_nodes():
    topology.assign_fog_nodes_to_zones(fog_node)

# Print zones and their fog nodes
for zone in zone_broadcaster.zones:
    print(f"{zone.name} x:{zone.x} y:{zone.y} coverage_radius:{zone.coverage_radius} covers nodes: {zone.fog_nodes}")


def step():
    for node in user_layer.get_nodes():
        time = Clock.time
        task = node.generate_task(time)
        topology.assign_task(node, task, zone_broadcaster)

    topology.update_topology()
    print("Iteration", i)
    for node in fog_layer.get_nodes():
        if len(node.tasks) > 0:
            print("Fog Node", node.id, "Tasks", len(node.tasks))
    for node in cloud_layer.get_nodes():
        if len(node.tasks) > 0:
            print("Cloud Node", node.id, "Tasks", len(node.tasks))
    print()


steps = 10
for i in range(steps):
    step()
