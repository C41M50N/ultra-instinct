from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Callable


class CameraState(IntEnum):
    CLEAR = 1
    STOP_SIGN = 2
    RED_LIGHT = 3
    GREEN_LIGHT = 4
    
class CarState(IntEnum):
    DRIVING = 1
    STOP = 2
    
@dataclass
class Registration:
    state: CarState
    action: 

class Controller:
    def __init__(self, camera_state: CameraState = CameraState.CLEAR, car_state: CarState = CarState.DRIVING):
        self.camera_state = camera_state
        self.car_state = car_state
        self.registrations: dict[CarState, list[Callable[[Any], Any]]] = {}
        
    def register(self, state: CarState, action: Callable[[Any], Any]):
        self.registrations[state].append(action)
        
    def set_state(self, state: CarState):
        self.car_state = state
        for action in self.registrations[state]:
            action()
        
