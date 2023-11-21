from enum import Enum

class PowerState(Enum):
    ON = 1
    OFF = 0

class RelayState(Enum):
    ENABLED = 1
    DISABLED = 0

class FanCoilMode(Enum):
    HEATER = 1
    AIRCONDITIONER = 2