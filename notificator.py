import json

import boto3

from config import get_property
from model import TaskAssignment

sqs = boto3.resource("sqs")
task_status_changed_queue = sqs.Queue(get_property("task_status_changed_queue_url"))


def notify(task: TaskAssignment):
    json_task = task.to_json()

    task_status_changed_queue.send_message(
        MessageBody=json.dumps(json_task),
    )
