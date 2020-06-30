import json
import uuid
from typing import Any, Dict, Union

import boto3

from config import get_property
from model import TaskAssignment, Status
from notificator import notify

dynamo = boto3.resource("dynamodb")
task_table = dynamo.Table(get_property("task_table_name"))


def assign_task(event: Dict[str, Any], context: Any) -> Dict[str, Union[str, int]]:
    try:
        return process(event)
    except Exception as e:
        print(f"Exception: {e}")
        return {
            "statusCode": 500,
            "body": str(e),
        }


def process(event: Dict[str, Any]) -> Dict[str, Any]:
    task = TaskAssignment.from_json(event["body"])
    task.status = Status.IN_PROGRESS
    task.active = True
    task.task_id = str(uuid.uuid4())

    json_task = task.to_json()

    task_table.put_item(
        Item=json_task,
    )
    notify(task)

    return {
        "statusCode": 200,
        "body": json.dumps(json_task),
    }
