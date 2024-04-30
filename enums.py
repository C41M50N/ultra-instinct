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
class StopCriteria:
    cls: Cls
    command: Command
    width: float
    time: float | None


STOP_CRITERIA = {
    Cls.STOP_SIGN: StopCriteria(Cls.STOP_SIGN, Command.STOP, 70, 5),
    Cls.RED_LIGHT: StopCriteria(Cls.RED_LIGHT, Command.STOP, 30, None),
    Cls.GREEN_LIGHT: StopCriteria(Cls.GREEN_LIGHT, Command.GO, 10, None),
    Cls.CLEAR: StopCriteria(Cls.CLEAR, Command.GO, None, None),
}
