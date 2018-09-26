# NOTE: this is for VESC firmware 3.33 
# ( https://github.com/tlalexander/bldc/tree/e74d3a3e4c2047b239084c152b4cbfddafbe3145 )

from pyvesc.messages.base import VESCMessage

class GetValues(metaclass=VESCMessage):
    """ Gets internal sensor data
    """
    id = 4

    fields = [
            ('temp_fet_filtered', 'e', 1),
            ('temp_motor_filtered', 'e', 1),
            ('avg_motor_current', 'f', 1),
            ('avg_input_current', 'f', 1),
            ('avg_id', 'f', 1),
            ('avg_iq', 'f', 1),
            ('duty_cycle_now',  'e', 1),
            ('rpm', 'f', 1),
            ('input_voltage', 'e', 1),
            ('amp_hours',  'f', 1),
            ('amp_hours_charged',  'f', 1),
            ('watt_hours', 'f', 1),
            ('watt_hours_charged', 'f', 1),
            ('tachometer_value', 'i', 1),
            ('tachometer_abs', 'i', 1)
    ]


class GetRotorPosition(metaclass=VESCMessage):
    """ Gets rotor position data
    
    Must be set to DISP_POS_MODE_ENCODER or DISP_POS_MODE_PID_POS (Mode 3 or 
    Mode 4). This is set by SetRotorPositionMode (id=21).
    """
    id = 39

    fields = [
            ('rotor_pos', 'i', 1)
    ]
