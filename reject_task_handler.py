import json
from typing import Any, Dict, Union

import boto3

from config import get_property
from model import TaskAssignment, Status
from notificator import notify

dynamo = boto3.resource("dynamodb")
task_table = dynamo.Table(get_property("task_table_name"))

sqs = boto3.resource("sqs")
task_status_changed_queue = sqs.Queue(get_property("task_status_changed_queue_url"))


def reject_task(event: Dict[str, Any], context: Any) -> Dict[str, Union[str, int]]:
    try:
        return process(event)
    except Exception as e:
        print(f"Exception: {e}")
        return {
            "statusCode": 500,
            "body": str(e),
        }


def process(event: Dict[str, Any]) -> Dict[str, Any]:
    task_id = event["pathParameters"]["task_id"]

    db_item = task_table.get_item(
        Key={
            "task_id": task_id,
        },
    )
    if db_item is None or "Item" not in db_item:
        raise Exception(f"Task with id {task_id} doesn't exist. Cannot reject this task.")

    task = TaskAssignment.from_json(db_item["Item"])

    if task.status != Status.FINISHED:
        raise Exception(f"Tasks in status {task.status} cannot be rejected.")

    task.status = Status.REJECTED
    json_task = task.to_json()

    task_table.put_item(
        Item=json_task,
    )
    notify(task)

    return {
        "statusCode": 200,
        "body": json.dumps(json_task),
    }
