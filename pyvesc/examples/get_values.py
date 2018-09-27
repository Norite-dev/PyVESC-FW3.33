import pyvesc
from pyvesc import GetFirmwareVersion, GetValues, SetRPM, SetCurrent, SetRotorPositionMode, GetRotorPosition, SetDutyCycle
import serial
import time
import matplotlib.pyplot as plt
import numpy as np

# Set your serial port here (either /dev/ttyX or COMX)
#serialport = '/dev/tty.usbmodem301'
serialport = 'COM5'

print("port " + serialport)


def get_values_example():    
    x = np.linspace(0, 100, 100)
    y1 = np.linspace(0, 0, 100)
    y2 = np.linspace(0, 0, 100)
    y3 = np.linspace(0, 0, 100)

    # You probably won't need this if you're embedding things in a tkinter plot...
    plt.ion()

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('voltage (V)', color='r')
    ax1.set_ylim(0, 40)

    ax2 = ax1.twinx()
    ax2.set_ylabel('current (A)', color='g')
    ax2.set_ylim(0, 40)

    ax3 = ax2.twinx()
    ax3.set_ylabel('rpm', color='b')
    ax3.set_ylim(0, 10000)

    line1, = ax1.plot(x, y1, 'r-') # Returns a tuple of line objects, thus the comma
    line2, = ax2.plot(x, y2, 'g-') # Returns a tuple of line objects, thus the comma
    line3, = ax3.plot(x, y3, 'b-') # Returns a tuple of line objects, thus the comma
    ax1.grid()
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    rpm = 0
    voltage = 0
    current = 0
    
    inbuf = b''    
    nextPingTime = time.time() + 2.0
    
    with serial.Serial(serialport, baudrate=115200, timeout=0.05) as ser:
        try:
            ser.flushInput()
            ser.flushOutput()
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
                # Send SetDutyCycle (100% = 100000)
                  #ser.write(pyvesc.encode(SetDutyCycle(5000)))  
                  # plot
                  y1 = y1[1:]
                  y1 = np.append(y1, voltage)
                  line1.set_ydata(y1)
                  
                  y2 = y2[1:]
                  y2 = np.append(y2, current)
                  line2.set_ydata(y2)
                  
                  y3 = y3[1:]
                  y3 = np.append(y3, rpm)
                  line3.set_ydata(y3)                      
                  
                  fig.canvas.draw()
                  fig.canvas.flush_events()

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
                              rpm = response.rpm
                              voltage = response.input_voltage
                              current = response.avg_motor_current
                              print("T: " + str(response.temp_fet_filtered) + " rpm: "+  str(response.rpm) + " volt: " + str(response.input_voltage) + " curr: " +str(response.avg_motor_current) + " Tachometer:" + str(response.tachometer_value) + " Tachometer ABS:" + str(response.tachometer_abs_value) + " Duty:" + str(response.duty_cycle_now) + " Watt Hours:" + str(response.watt_hours) + " Watt Hours Charged:" + str(response.watt_hours_charged)  )
                              
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
            print ("turning off the VESC...")
            ser.write(pyvesc.encode(SetCurrent(0)))            
            ser.flushOutput()
            ser.flushInput()
            

if __name__ == "__main__":
    #signal.signal(signal.SIGINT, signal_handler)
    get_values_example()

    
