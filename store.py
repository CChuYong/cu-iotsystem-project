from common import RelayState, PowerState, FanCoilMode
import temp

current_relay_state = RelayState.DISABLED
current_power_state = PowerState.OFF
desired_temp = 20.0
current_temperature = 0.0
fancoil_mode = FanCoilMode.HEATER

def create_summary():
    return {
        'relayState': current_relay_state.name,
        'powerState': current_power_state.name,
        'desiredTemp': desired_temp,
        'currentTemp': current_temperature,
        'mode': fancoil_mode.name
        }