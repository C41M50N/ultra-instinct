from dataclasses import dataclass
from enum import IntEnum


class Cls(IntEnum):
    STOP_SIGN = 0
    RED_LIGHT = 1
    GREEN_LIGHT = 2
    CLEAR = 3


class Command(IntEnum):
    STOP = 1
    GO = 2


@dataclass
class Message:
    command: Command
    time: float
