import random
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def generate_fixed_fog_nodes(num_nodes, filename, power_range=(10, 100), position_range=(0, 1000), coverage_range=(150, 200)):
    root = ET.Element('fcd-export')

    for node_id in range(1, num_nodes + 1):
        fog_node_elem = ET.SubElement(root, 'nodes', {
            'id': f"fixedFog{node_id}",
            'x': f"{random.uniform(*position_range):.2f}",
            'y': f"{random.uniform(*position_range):.2f}",
            'type': 'fixedFog',
            'power': f"{random.uniform(*power_range):.2f}",
            'lane': f"{random.randint(4, 6)}",
            'coverage_radius': f"{random.uniform(*coverage_range):.2f}"
        })

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_as_string)

num_nodes = 10
filename = 'D:\\fixedFogNodes_data.xml'

generate_fixed_fog_nodes(num_nodes, filename, power_range=(10, 100), position_range=(0, 1000), coverage_range=(150, 200))
print(f"Data successfully saved to {filename}.")