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

def generate_vehicle_data(num_timesteps, num_vehicles, vehicle_types, filename, 
                          speed_change_range=(-5, 5), angle_change_range=(-20, 20), movement_range=(-1000, 1000)):
    root = ET.Element('fcd-export')

    vehicles = {f"veh{vehicle_id}": {
        'x': random.uniform(0, 1000),
        'y': random.uniform(0, 1000),
        'angle': random.uniform(0, 360),
        'type': random.choice(vehicle_types),
        'speed': random.uniform(5, 15),
        'pos': random.uniform(0, 100),
        'lane': random.randint(1, 3)
    } for vehicle_id in range(1, num_vehicles + 1)}

    for timestep in range(num_timesteps):
        time_step_elem = ET.SubElement(root, 'timestep', time=f"{timestep}.00")
        for vehicle_id, vehicle_data in vehicles.items():
            ET.SubElement(time_step_elem, 'vehicle', {
                'id': vehicle_id,
                'x': f"{vehicle_data['x']:.2f}",
                'y': f"{vehicle_data['y']:.2f}",
                'angle': f"{vehicle_data['angle']:.2f}",
                'type': vehicle_data['type'],
                'speed': f"{vehicle_data['speed']:.2f}",
                'pos': f"{vehicle_data['pos']:.2f}",
                'lane': f"{vehicle_data['lane']}"
            })

            vehicle_data['speed'], vehicle_data['angle'] = update_speed_and_angle(
                vehicle_data['speed'], vehicle_data['angle'], speed_change_range, angle_change_range
            )
            vehicle_data['x'], vehicle_data['y'] = random_movement(
                vehicle_data['x'], vehicle_data['y'], vehicle_data['speed'], vehicle_data['angle'], movement_range
            )
            vehicle_data['pos'] += vehicle_data['speed'] * 0.1

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_as_string)

vehicle_types = ['car', 'bus', 'truck']
num_timesteps = 100
num_vehicles = 100
filename = 'D:\\vehicles_data.xml'

generate_vehicle_data(num_timesteps, num_vehicles, vehicle_types, filename,
                      speed_change_range=(-5, 5), angle_change_range=(-20, 20), movement_range=(-1000, 1000))
print(f"Data successfully saved to {filename}.")