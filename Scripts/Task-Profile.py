import random
import xml.etree.ElementTree as ET
from xml.dom.minidom import parseString

def generate_tasks_data(num_seconds, num_tasks, num_creators, filename, power_range=(1, 10), size_range=(1, 10), deadline_range=(1, 10)):
    root = ET.Element('tasks')

    task_id = 1
    tasks_per_second = [0] * num_seconds
    for _ in range(num_tasks):
        tasks_per_second[random.randint(0, num_seconds - 1)] += 1

    creators = [f"veh{creator_id}" for creator_id in range(1, num_creators + 1)]
    active_tasks = {creator: [] for creator in creators}

    for second in range(num_seconds):
        for _ in range(tasks_per_second[second]):
            available_creators = [creator for creator, deadlines in active_tasks.items() if not deadlines or min(deadlines) > second]
            if not available_creators:
                continue
            creator = random.choice(available_creators)

            deadline = min(second + random.randint(*deadline_range), num_seconds - 1)
            task_elem = ET.SubElement(root, 'task', {
                'id': f"task{task_id}",
                'name': f"Task_{task_id}",
                'creation_time': f"{second}",
                'deadline': f"{deadline}",
                'power_needed': f"{random.uniform(*power_range):.2f}",
                'size': f"{random.uniform(*size_range):.2f}",
                'creator': creator
            })
            active_tasks[creator].append(deadline)
            task_id += 1

        for creator in active_tasks:
            active_tasks[creator] = [d for d in active_tasks[creator] if d > second]

    rough_string = ET.tostring(root, 'utf-8')
    reparsed = parseString(rough_string)
    pretty_xml_as_string = reparsed.toprettyxml(indent="  ")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(pretty_xml_as_string)

num_seconds = 100
num_tasks = 300
num_creators = 100
filename = 'D:\\tasks_data.xml'

generate_tasks_data(num_seconds, num_tasks, num_creators, filename, power_range=(1, 10), size_range=(1, 10), deadline_range=(1, 10))
print(f"Data successfully saved to {filename}.")