"""Module containing the SessionInfo dataclass"""

from dataclasses import dataclass
from datetime import timedelta
from typing import List

@dataclass
class SessionInfo():
    """Dataclass containing session information"""

    working_addresses: List[str]
    total_addresses: int
    responded_count: int
    not_responded_count: int
    active_time: timedelta
    max_threads: int
    active_threads: int

    def __str__(self) -> str:
        text = "                                                                     \n"
        text += f"Responded: {self.responded_count}, No response: {self.not_responded_count}, Total"
        text += f": {self.responded_count + self.not_responded_count}/{self.total_addresses}\n"
        text += f"Max Threads: {self.max_threads}, Active threads: {self.active_threads}\n"
        text += f"Elapsed: {str(self.active_time).split('.', maxsplit=1)[0]}\n"
        text += "                                                                     "
        return text
