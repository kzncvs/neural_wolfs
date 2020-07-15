import requests
import json

import config


def chunk(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


headers = {
    "Authorization": f'OAuth {config.toloka_token}',
    'Content-Type': 'application/JSON'
}

etalon_pool_id = config.toloka_etalon_pool_id
pool_data = requests.post(
    f'https://{config.toloka_api_url}/api/v1/pools/{etalon_pool_id}/clone',
    headers=headers
)
while pool_data.json()["status"] != "SUCCESS":
    pool_data = requests.get(
        f'https://{config.toloka_api_url}/api/v1/operations/{pool_data.json()["id"]}',
        headers=headers
    )
pool_id = pool_data.json()["details"]['pool_id']

with open(config.wolfs_from_vk_file, 'r') as file:
    pictures = json.loads(file.read())

tasks = [
    {
        "input_values": {
            "image": p["link"]
        }
    }
    for p in pictures
]

task_suites = chunk(tasks, config.toloka_tasksuite_size)

for ts in task_suites:
    task_suite = {
        "tasks": ts,
        "pool_id": pool_id
    }

    requests.post(
        f'https://{config.toloka_api_url}/api/v1/task-suites?allow_defaults=true',
        json=task_suite,
        headers=headers
    )

