# NOTE: this is for VESC firmware 3.33 
# ( https://github.com/tlalexander/bldc/tree/e74d3a3e4c2047b239084c152b4cbfddafbe3145 )

from pyvesc.messages.base import VESCMessage

class GetFirmwareVersion(metaclass=VESCMessage):        
    id = 0
    can_id = None

    fields = [
            ('version_major', 'b', 1),
            ('version_minor', 'b', 1)
    ]



class GetValues(metaclass=VESCMessage):    
    """ Gets internal sensor data
    """
    id = 4
    can_id = None

    fields = [
            ('temp_fet_filtered', 'H', 10),
            ('temp_motor_filtered', 'e', 1),
            ('avg_motor_current', 'i', 100),
            ('avg_input_current', 'f', 1),
            ('avg_id', 'f', 1),
            ('avg_iq', 'f', 1),
            ('duty_cycle_now',  'e', 1),
            ('rpm', 'i', 1),
            ('input_voltage', 'h', 10),
            ('amp_hours',  'f', 1),
            ('amp_hours_charged',  'f', 1),
            ('watt_hours', 'f', 1),
            ('watt_hours_charged', 'f', 1),
            ('tachometer_value', 'i', 1),
            ('tachometer_abs_value', 'i', 1),
            ('fault', 'b', 1)
    ]


class GetRotorPosition(metaclass=VESCMessage):
    """ Gets rotor position data
    
    Must be set to DISP_POS_MODE_ENCODER or DISP_POS_MODE_PID_POS (Mode 3 or 
    Mode 4). This is set by SetRotorPositionMode (id=21).
    """
    id = 22
    can_id = None

    fields = [
            ('rotor_pos', 'i', 1)
    ]
