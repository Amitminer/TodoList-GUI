import datetime
from typing import Optional

class Task:
    def __init__(self, text: str, status: str = "New", done: bool = False, date: Optional[str] = None, id: Optional[int] = None) -> None:
        """
        Initialize a Task object.

        :param text: The text description of the task.
        :param status: The status of the task (default is "New").
        :param done: Boolean indicating if the task is done (default is False).
        :param date: The date the task was created (default is None, will use the current date).
        :param id: The unique ID of the task (default is None).
        """
        self.id = id
        self.text = text
        self.status = status
        self.date = date or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Use current date and time
        self.done = done

    def toggle_done(self) -> None:
        """
        Toggle the done status of the task and update its status accordingly.
        """
        self.done = not self.done
        self.status = "Done" if self.done else "New"
