from common import RelayState, PowerState
import temp
current_relay_state = RelayState.DISABLED
current_power_state = PowerState.OFF

def create_summary():
    return {
        'relayState': current_relay_state.name,
        'powerState': current_power_state.name,
        'desiredTemp': temp.get_desired_temp(),
        'currentTemp': temp.get_current_temperature(),
        'mode': temp.get_fancoil_mode().name
        }