import random
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString
from math import cos, sin, radians

def random_movement(x, y, speed, angle, movement_range):
    rad = radians(angle)
    new_x = x + speed * cos(rad)
    new_y = y + speed * sin(rad)
    new_x = max(min(new_x, movement_range[1]), movement_range[0])
    new_y = max(min(new_y, movement_range[1]), movement_range[0])
    return new_x, new_y

def update_speed_and_angle(speed, angle, speed_change_range, angle_change_range):
    speed_change = random.uniform(*speed_change_range)
    angle_change = random.uniform(*angle_change_range)
    new_speed = max(0, speed + speed_change)
    new_angle = (angle + angle_change) % 360
    return new_speed, new_angle

def update_lane(lane, lane_change_range):
    lane_change = random.randint(*lane_change_range)
    new_lane = max(1, min(lane + lane_change, 3))
    return new_lane

def generate_fog_node_data(num_timesteps, num_nodes, filename, 
                           speed_change_range=(-5, 5), angle_change_range=(-20, 20), 
                           movement_range=(-1000, 1000), lane_change_range=(-1, 1), power_range=(10, 100)):
    root = ET.Element('fcd-export')

    fog_nodes = {f"fog{node_id}": {
        'x': random.uniform(0, 1000),
        'y': random.uniform(0, 1000),
        'angle': random.uniform(0, 360),
        'type': 'mobileFog',
        'speed': random.uniform(5, 15),
        'pos': random.uniform(0, 100),
        'lane': random.randint(1, 3),
        'power': random.uniform(*power_range)
    } for node_id in range(1, num_nodes + 1)}

    for timestep in range(num_timesteps):
        time_step_elem = ET.SubElement(root, 'timestep', time=f"{timestep}.00")
        for node_id, node_data in fog_nodes.items():
            ET.SubElement(time_step_elem, 'vehicle', {
                'id': node_id,
                'x': f"{node_data['x']:.2f}",
                'y': f"{node_data['y']:.2f}",
                'angle': f"{node_data['angle']:.2f}",
                'type': node_data['type'],
                'speed': f"{node_data['speed']:.2f}",
                'pos': f"{node_data['pos']:.2f}",
                'lane': f"{node_data['lane']}",
                'power': f"{node_data['power']:.2f}"
            })

            node_data['speed'], node_data['angle'] = update_speed_and_angle(
                node_data['speed'], node_data['angle'], speed_change_range, angle_change_range
            )
            node_data['x'], node_data['y'] = random_movement(
                node_data['x'], node_data['y'], node_data['speed'], node_data['angle'], movement_range
            )
            node_data['pos'] += node_data['speed'] * 0.1
            node_data['lane'] = update_lane(node_data['lane'], lane_change_range)

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_as_string)

num_timesteps = 100
num_nodes = 100
filename = 'D:\\mobileFogNodes_data.xml'

generate_fog_node_data(num_timesteps, num_nodes, filename,
                       speed_change_range=(-5, 5), angle_change_range=(-20, 20),
                       movement_range=(-1000, 1000), lane_change_range=(-1, 1), power_range=(10, 100))
print(f"Data successfully saved to {filename}.")