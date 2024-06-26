from Topology import Topology
from UsersLayer import UsersLayer
from FogLayer import FogLayer
from CloudLayer import CloudLayer
from Node import Node, Layer
from Graph import MobilityGraph

fog_layer = FogLayer()
for i in range(5):
    fog_layer.add_node(Node(i, Layer.Fog, cpu_freq=2, x=i * 20, y=i * 20, coverage_radius=40))

cloud_layer = CloudLayer()
cloud_layer.add_node(Node(0, Layer.Cloud, cpu_freq=2, x=0, y=0, coverage_radius=50))

graph = MobilityGraph(xml_path="fcd_output.xml")
user_layer = UsersLayer(graph)

topology = Topology(user_layer, fog_layer, cloud_layer, graph)


def step():
    for node in user_layer.get_nodes():
        time = graph.current_time
        task = node.generate_task(time)
        topology.assign_task(node, task)

    topology.update_topology()
    print("Iteration", i)
    for node in fog_layer.get_nodes():
        print("Fog Node", node.id, "Tasks", len(node.tasks))
    for node in cloud_layer.get_nodes():
        print("Cloud Node", node.id, "Tasks", len(node.tasks))
    print()


steps = 10
for i in range(steps):
    step()
