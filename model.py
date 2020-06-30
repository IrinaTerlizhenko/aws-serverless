import json
from enum import Enum
from typing import Union, Dict, Any


class Status(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"
    REJECTED = "REJECTED"
    CLOSED = "CLOSED"


class TaskAssignment:
    def __init__(
            self,
            task_id: str,
            mentor: str,
            mentee: str,
            mentor_email: str,
            mentee_email: str,
            status: Status,
            active: bool,
    ) -> None:
        self._task_id = task_id
        self._mentor = mentor
        self._mentee = mentee
        self._mentor_email = mentor_email
        self._mentee_email = mentee_email
        self._status = status
        self._active = active

    @staticmethod
    def from_json(data: Union[str, Dict[str, Any]]):
        if type(data) == str:
            data = json.loads(data)
        status = data.get("status")
        return TaskAssignment(
            data.get("task_id"),
            data["mentor"],
            data["mentee"],
            data["mentor_email"],
            data["mentee_email"],
            Status(status) if status else None,
            data.get("active")
        )

    def to_json(self):
        return {
            "task_id": self._task_id,
            "mentor": self._mentor,
            "mentee": self._mentee,
            "mentor_email": self._mentor_email,
            "mentee_email": self._mentee_email,
            "status": self._status.value,
            "active": self._active,
        }

    @property
    def task_id(self) -> str:
        return self._task_id

    @task_id.setter
    def task_id(self, value: str) -> None:
        self._task_id = value

    @property
    def mentor(self) -> str:
        return self._mentor

    @property
    def mentee(self) -> str:
        return self._mentee

    @property
    def mentor_email(self) -> str:
        return self._mentor_email

    @property
    def mentee_email(self) -> str:
        return self._mentee_email

    @property
    def status(self) -> Status:
        return self._status

    @status.setter
    def status(self, value: Status) -> None:
        self._status = value

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        self._active = value
