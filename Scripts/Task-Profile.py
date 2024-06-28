import random
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def generate_tasks_data(num_seconds, num_tasks, filename, power_range=(1, 10), size_range=(1, 10), deadline_range=(1, 10)):
    root = ET.Element('tasks')

    task_id = 1
    tasks_per_second = [0] * num_seconds
    for _ in range(num_tasks):
        tasks_per_second[random.randint(0, num_seconds - 1)] += 1

    for second in range(num_seconds):
        for _ in range(tasks_per_second[second]):
            task_elem = ET.SubElement(root, 'task', {
                'id': f"task{task_id}",
                'name': f"Task_{task_id}",
                'creation_time': f"{second}",
                'deadline': f"{second + random.randint(*deadline_range)}",
                'power_needed': f"{random.uniform(*power_range):.2f}",
                'size': f"{random.uniform(*size_range):.2f}"
            })
            task_id += 1

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_as_string)

num_seconds = 100
num_tasks = 300
filename = 'D:\\tasks_data.xml'

generate_tasks_data(num_seconds, num_tasks, filename, power_range=(1, 10), size_range=(1, 10), deadline_range=(1, 10))
print(f"Data successfully saved to {filename}.")