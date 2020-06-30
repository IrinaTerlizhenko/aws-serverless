import os
from typing import Any, Dict, List

import boto3

from model import TaskAssignment, Status

ses_client = boto3.client("ses")

EMAIL_FROM = os.getenv("EMAIL_FROM")


def notify(event: Dict[str, Any], context: Any) -> None:
    try:
        return process(event)
    except Exception as e:
        print(f"Exception: {e}")


def process(event: Dict[str, Any]) -> None:
    records: List[Dict[str, Any]] = event["Records"]
    for record in records:
        task = TaskAssignment.from_json(record["body"])

        if task.status == Status.IN_PROGRESS:
            destination = {
                "ToAddresses": [
                    task.mentee_email,
                ],
                "CcAddresses": [
                    task.mentor_email,
                ],
            }
            subject = "[Mentoring] New Task Assigned"
            text = f"Hi {task.mentee}!\n" \
                   f"\n" \
                   f"A new task has been assigned to you.\n" \
                   f"Mentor: {task.mentor}."
        elif task.status == Status.FINISHED:
            destination = {
                "ToAddresses": [
                    task.mentor_email,
                ],
            }
            subject = "[Mentoring] Task Finished and Waiting For Review"
            text = f"Hi {task.mentor}!\n" \
                   f"\n" \
                   f"The task {task.task_id} is finished and waiting for your review.\n" \
                   f"Mentee: {task.mentee}."
        elif task.status == Status.CLOSED:
            destination = {
                "ToAddresses": [
                    task.mentee_email,
                ],
                "CcAddresses": [
                    task.mentor_email,
                ],
            }
            subject = "[Mentoring] Task Closed"
            text = f"Hi {task.mentee}!\n" \
                   f"\n" \
                   f"The task {task.task_id} has been approved by your mentor and closed."
        elif task.status == Status.REJECTED:
            destination = {
                "ToAddresses": [
                    task.mentee_email,
                ],
                "CcAddresses": [
                    task.mentor_email,
                ],
            }
            subject = "[Mentoring] Task Rejected"
            text = f"Hi {task.mentee}!\n" \
                   f"\n" \
                   f"The task {task.task_id} has been rejected by your mentor." \
                   f" It can be resend once you fix all comments."
        else:
            raise Exception(f"Tasks in status {task.status} are not eligible for notification.")

        ses_client.send_email(
            Source=EMAIL_FROM,
            Destination=destination,
            Message={
                "Subject": {
                    "Data": subject,
                    "Charset": "utf-8",
                },
                "Body": {
                    "Text": {
                        "Data": f"{text}\n"
                                f"\n"
                                f"Best Regards,\n"
                                f"Mentoring Team",
                        "Charset": "utf-8",
                    },
                }
            },
        )
