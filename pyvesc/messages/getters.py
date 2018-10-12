# NOTE: this is for VESC firmware 3.33 
# ( https://github.com/tlalexander/bldc/tree/e74d3a3e4c2047b239084c152b4cbfddafbe3145 )

from pyvesc.messages.base import VESCMessage


class GetConfig(metaclass=VESCMessage):
    id = 14 # COMM_GET_MCCONF
    can_id = None
    
    fields = [
            ('pwm_mode', 'B'),            
            ('comm_mode', 'B'),            
            ('motor_type', 'B'),            
            ('sensor_mode', 'B'),            
            ('l_current_max', 'f'),                        
            ('l_current_min', 'f'),                        
            ('l_in_current_max', 'f'),                        
            ('l_in_current_min', 'f'),                        
            ('l_abs_current_max', 'f'),                        
            ('l_min_erpm', 'f'),                        
            ('l_max_erpm', 'f'),                        
            ('l_erpm_start', 'f'),                        
            ('l_max_erpm_fbrake', 'f'),                        
            ('l_max_erpm_fbrake_cc', 'f'),                        
            ('l_min_vin', 'f'),                        
            ('l_max_vin', 'f'),                        
            ('l_battery_cut_start', 'f'),                        
            ('l_battery_cut_end', 'f'),                        
            ('l_slow_abs_current', 'B'),                        
            ('l_temp_fet_start', 'f'),                        
            ('l_temp_fet_end', 'f'),                        
            ('l_temp_motor_start', 'f'),                        
            ('l_temp_motor_end', 'f'),                        
            ('l_temp_accel_dec', 'f'),                        
            ('l_min_duty', 'f'),                        
            ('l_max_duty', 'f'),                        
            ('l_watt_max', 'f'),                        
            ('l_watt_min', 'f'),                        
            ('sl_min_erpm', 'f'),                        
            ('sl_min_erpm_cycle_int_limit', 'f'),                        
            ('sl_max_fullbreak_current_dir_change', 'f'),                        
            ('sl_cycle_int_limit', 'f'),                        
            ('sl_phase_advance_at_br', 'f'),                        
            ('sl_cycle_int_rpm_br', 'f'),                                    
            ('sl_bemf_coupling_k', 'f'),                                    
            ('hall_table_0', 'b'),                                    
            ('hall_table_1', 'b'),                                    
            ('hall_table_2', 'b'),                                    
            ('hall_table_3', 'b'),                                    
            ('hall_table_4', 'b'),                                    
            ('hall_table_5', 'b'),                                    
            ('hall_table_6', 'b'),                                    
            ('hall_table_7', 'b'),                                    
            ('hall_sl_erpm', 'f'),                                    
            ('foc_current_kp', 'f'),                                    
            ('foc_current_ki', 'f'),                                                
            ('foc_f_sw', 'f'),                                                
            ('foc_dt_us', 'f'),                                                
            ('foc_encoder_inverted', 'B'),                                                
            ('foc_encoder_offset', 'f'),                                                
            ('foc_encoder_ratio', 'f'),                                                
            ('foc_sensor_mode', 'B'),                                                
            ('foc_pll_kp', 'f'),                                                
            ('foc_pll_ki', 'f'),                                                
            ('foc_motor_l', 'f'),                                                
            ('foc_motor_r', 'f'),                                                
            ('foc_motor_flux_linkage', 'f'),                                                
            ('foc_observer_gain', 'f'),                                                
            ('foc_observer_gain_slow', 'f'),                                                
            ('foc_duty_dowmramp_kp', 'f'),                                                
            ('foc_duty_dowmramp_ki', 'f'),                                                          
            ('foc_openloop_rpm', 'f'),                                                
            ('foc_sl_openloop_hyst', 'f'),                                                
            ('foc_sl_openloop_time', 'f'),                                                
            ('foc_sl_d_current_duty', 'f'),                                                
            ('foc_sl_d_current_factor', 'f'),                                                
            ('foc_hall_table_0', 'B'),                                                
            ('foc_hall_table_1', 'B'),                                                
            ('foc_hall_table_2', 'B'),                                                
            ('foc_hall_table_3', 'B'),                                                
            ('foc_hall_table_4', 'B'),                                                
            ('foc_hall_table_5', 'B'),                                                
            ('foc_hall_table_6', 'B'),                                                
            ('foc_hall_table_7', 'B'),                                                            
            ('foc_sl_erpm', 'f'),                                                
            ('foc_sample_v0_v7', 'B'),                                                
            ('foc_sample_high_current', 'B'),                                                
            ('foc_sat_comp', 'f'),                                                
            ('foc_temp_comp', 'B'),                                                
            ('foc_temp_comp_base_temp', 'f'),                                                
            ('s_pid_kp', 'f'),                                                
            ('s_pid_ki', 'f'),                                                
            ('s_pid_kd', 'f'),                                                
            ('s_pid_min_erpm', 'f'),                                                
            ('s_pid_allow_braking', 'B'),                                                
            ('p_pid_kp', 'f'),                                                
            ('p_pid_ki', 'f'),                                                
            ('p_pid_kd', 'f'),                                                
            ('p_pid_ang_div', 'f'),                                                
            ('cc_startup_boost_duty', 'f'),                                                
            ('cc_min_current', 'f'),                                                
            ('cc_gain', 'f'),                                                
            ('cc_ramp_step_max', 'f'),                                                
            ('m_fault_stop_time_ms', 'i'),                                                
            ('m_duty_ramp_step', 'f'),                                                
            ('m_current_backoff_gain', 'f'),                                                
            ('m_encoder_counts', 'I'),                                                
            ('m_sensor_port_mode', 'B'),                                                
            ('m_invert_direction', 'B'),                                                
            ('m_drv8301_oc_mode', 'B'),                                                
            ('m_drv8301_oc_adj', 'B'),                                                
            ('m_bldc_f_sw_min', 'f'),                                                
            ('m_bldc_f_sw_max', 'f'),                                                
            ('m_dc_f_sw', 'f'),                                                
            ('m_ntc_motor_beta', 'f'),                                                            
    ]


class GetPrint(metaclass=VESCMessage):        
    id = 21 # COMM_PRINT
    can_id = None

    fields = [
            ('msg', 's'),            
    ]

  

class GetFirmwareVersion(metaclass=VESCMessage):        
    id = 0 # COMM_FW_VERSION 
    can_id = None

    fields = [
            ('version_major', 'b', 1),
            ('version_minor', 'b', 1)
    ]



class GetValues(metaclass=VESCMessage):    
    """ Gets internal sensor data
    """
    id = 4 #  COMM_GET_VALUES
    can_id = None

    fields = [
            ('temp_fet_filtered', 'H', 10),
            ('temp_motor_filtered', 'e', 1),
            ('avg_motor_current', 'i', 100),
            ('avg_input_current', 'i', 100),
            ('avg_id', 'f', 1),
            ('avg_iq', 'f', 1),
            ('duty_cycle_now', 'h', 10),
            ('rpm', 'i', 1),
            ('input_voltage', 'h', 10),
            ('amp_hours',  'i', 10000),
            ('amp_hours_charged',  'i', 10000),
            ('watt_hours', 'i', 10000),
            ('watt_hours_charged', 'i', 10000),
            ('tachometer_value', 'i', 1),
            ('tachometer_abs_value', 'i', 1),
            ('fault', 'b', 1)
    ]


class GetRotorPosition(metaclass=VESCMessage):
    """ Gets rotor position data
    
    Must be set to DISP_POS_MODE_ENCODER or DISP_POS_MODE_PID_POS (Mode 3 or 
    Mode 4). This is set by SetRotorPositionMode (id=21).
    """
    id = 22  # COMM_ROTOR_POSITION
    can_id = None

    fields = [
            ('rotor_pos', 'i', 100000)
    ]

class GetRotorPositionCumulative(metaclass=VESCMessage):    
    id = 38  # COMM_ROTOR_POSITION_CUMULATIVE
    can_id = None

    fields = [
            ('rotor_pos', 'i', 1)
    ]

        