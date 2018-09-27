import pyvesc
from pyvesc import GetFirmwareVersion, GetValues, SetRPM, SetCurrent, SetRotorPositionMode, GetRotorPosition
import serial
import time

# Set your serial port here (either /dev/ttyX or COMX)
#serialport = '/dev/tty.usbmodem301'
serialport = 'COM5'

print("port " + serialport)

def get_values_example():    
    inbuf = b''
    nextPingTime = time.time() + 2.0
    
    with serial.Serial(serialport, baudrate=115200, timeout=0.05) as ser:
        try:
            # Optional: Turn on rotor position reading if an encoder is installed
            ser.write(pyvesc.encode_request(GetFirmwareVersion))                                    
            #ser.write(pyvesc.encode(SetRotorPositionMode(SetRotorPositionMode.DISP_POS_OFF)))                        
            while True:
                # Set the ERPM of the VESC motor
                #    Note: if you want to set the real RPM you can set a scalar
                #          manually in setters.py
                #          12 poles and 19:1 gearbox would have a scalar of 1/228                

                # Request the current measurement from the vesc                                
                if time.time() > nextPingTime:
                  nextPingTime = time.time() + 0.5
                  ser.write(pyvesc.encode_request(GetValues))                                
                  ser.write(pyvesc.encode(SetRPM(3000)))            

                time.sleep(0.01)
                
                # Check if there is enough data back for a measurement
                if ser.in_waiting > 0:                   
                  inbuf += ser.read(ser.in_waiting)                 
                if len(inbuf) > 59:
                    (response, consumed) = pyvesc.decode(inbuf)
                    if consumed > 0:                
                        #print("consumed " + str(consumed))                
                        inbuf = inbuf[consumed:]
                        # Print out the values
                        try:                                                
                            #print("response " + str(response.id))
                            if isinstance(response, GetFirmwareVersion):
                              print("Firmware: " + str(response.version_major) + ", " + str(response.version_minor))
                            elif isinstance(response, GetValues):
                              print("rpm: "+  str(response.rpm) + " volt: " + str(response.input_voltage) + " curr: " +str(response.avg_motor_current)  )
                              
                        except:
                            # ToDo: Figure out how to isolate rotor position and other sensor data
                            #       in the incoming datastream
                            #try:
                            #    print(response.rotor_pos)
                            #except:
                            #    pass
                            pass

                  

        except KeyboardInterrupt:
            # Turn Off the VESC
            ser.write(pyvesc.encode(SetCurrent(0)))
            pass

if __name__ == "__main__":
    get_values_example()
