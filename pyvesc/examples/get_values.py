import pyvesc
from pyvesc import GetFirmwareVersion, GetValues, SetRPM, SetCurrent, SetRotorPositionMode, GetRotorPosition, SetDutyCycle, SetPosition, GetRotorPositionCumulative, SetCurrentGetPosCumulative, SetPositionCumulative, SetTerminalCommand, GetPrint, GetConfig, SetConfig, SetAlive
import serial
import os
import math
import time
import matplotlib.pyplot as plt
import numpy as np
import struct
from xml.dom import minidom

# Set your serial port here (either /dev/ttyX or COMX)
#serialport = '/dev/tty.usbmodem301'
serialport = 'COM7'

print("port " + serialport)


def dump(cfg):
   for attr in cfg._field_names:
       if hasattr( cfg, attr ):
           print( "cfg.%s = %s" % (attr, getattr(cfg, attr)))
           

def test(*args):
  for arg in args:
    print(arg)

           
def sendConfig(ser):    
    if not os.path.exists('motor1.xml'): 
      print("no config file found => skipping sendConfig...")
      return
    doc = minidom.parse('motor1.xml')               
    count = 0
    values = []
    for field in SetConfig.fields:
      key = field[0]
      fmt = field[1]
      #print(key)
      item = doc.getElementsByTagName(key)
      if (len(item) > 0):
        value = item[0].firstChild.data
        if (fmt=='B') : value = int(value)
        if (fmt=='b') : value = int(value)
        if (fmt=='i') : value = int(value)
        if (fmt=='I') : value = int(value)
        if (fmt=='f') : value = float(value) 
        try:
          struct.pack(fmt, value)
        except Exception as e:
          print("ERROR! " + key + " ["+fmt+"]" + " = " + str(value) + ": " + str(e))
        values.append(value)
        count=count+1
      else:
        print("error finding field in config: "+field[0])
    print("found config fields: "+str(count))
    ser.write(pyvesc.encode(SetConfig(*values)))                            
    print("config sent")
    #test(*values)
    


def get_values_example():    
    #  
    #  choose VESC control mode:
    #    True: position control
    #    False: speed control
    POS_CONTROL = True
    
    x = np.linspace(0, 100, 100)
    y1 = np.linspace(0, 0, 100)
    y2 = np.linspace(0, 0, 100)
    y3 = np.linspace(0, 0, 100)
    y4 = np.linspace(0, 0, 100)    

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
    ax3.set_ylabel('rpm/pos', color='b')    
    if POS_CONTROL == True:
      ax3.set_ylim(0, 360*10)   # angle range    
    else:
      ax3.set_ylim(0, 10000) # rpm range      
          
    line1, = ax1.plot(x, y1, 'r-') # Returns a tuple of line objects, thus the comma
    line2, = ax2.plot(x, y2, 'g-') # Returns a tuple of line objects, thus the comma
    line3, = ax3.plot(x, y3, 'b-') # Returns a tuple of line objects, thus the comma
    line4, = ax3.plot(x, y4, 'y-') # Returns a tuple of line objects, thus the comma
    ax1.grid()
    fig.canvas.draw()
    fig.canvas.flush_events()
        
    rpm = 0    
    pos = 0
    set_rpm = 1000
    set_pos = 0
    voltage = 0
    current = 0    
    
    inbuf = b''    
    nextCmdTime = time.time() + 2.0
    nextPlotTime = time.time()
    nextInfoTime = time.time()
    
    with serial.Serial(serialport, baudrate=115200, timeout=0) as ser:
        try:
            ser.flushInput()
            ser.flushOutput()
            # Optional: Turn on rotor position reading if an encoder is installed
            ser.write(pyvesc.encode_request(GetFirmwareVersion))                                                                        
            #ser.write(pyvesc.encode_request(GetConfig))                                                                        
            sendConfig(ser)
            #ser.write(pyvesc.encode(SetRotorPositionMode(SetRotorPositionMode.DISP_POS_OFF)))                 
            ser.write(pyvesc.encode(SetRotorPositionMode(SetRotorPositionMode.DISP_POS_MODE_ENCODER)))                        
            #ser.write(pyvesc.encode(SetRotorPositionMode(SetRotorPositionMode.DISP_POS_MODE_OBSERVER)))                                    
            #ser.write(pyvesc.encode(SetRotorPositionMode(SetRotorPositionMode.DISP_POS_MODE_PID_POS)))
            
            ser.write(pyvesc.encode(SetTerminalCommand('ping')))                        
            
            
            while True:
                # Set the ERPM of the VESC motor
                #    Note: if you want to set the real RPM you can set a scalar
                #          manually in setters.py
                #          12 poles and 19:1 gearbox would have a scalar of 1/228                

                # Request the current measurement from the vesc                                                
                
                if time.time() > nextInfoTime:
                  nextInfoTime = time.time() + 0.2                                                     
                  ser.write(pyvesc.encode_request(GetValues))                                
                  ser.write(pyvesc.encode(SetAlive))                                                  
                  #ser.write(pyvesc.encode_request(SetCurrentGetPosCumulative(20)))                                
                
                if time.time() > nextCmdTime:
                  nextCmdTime = time.time() + 2.0  # next command after 2 seconds
                  if POS_CONTROL == True:                                      
                    #set_pos = math.sin(time.time() % 10.0 / 10.0 * 2 * math.pi) * 1800 + 1800                     
                    #set_pos = math.sin(time.time() % 10.0 / 10.0 * 2 * math.pi) * 180 + 180
                    set_pos = (set_pos + 100) % 3600   # increase angle by 100 degree, overflow at 3600 degree
                    #ser.write(pyvesc.encode(SetPosition(set_pos))) # degree                                        
                    if set_rpm == 1000:  # toggle speed between 1000 and 3000
                      set_rpm == 3000
                    else:
                      set_rpm == 1000
                    ser.write(pyvesc.encode_request(SetPositionCumulative(set_pos, 0))) # degree, erpm                                         
                  else:
                    ser.write(pyvesc.encode(SetRPM(set_rpm)))                  
                  # Send SetDutyCycle (100% = 100000)
                  #ser.write(pyvesc.encode(SetDutyCycle(5000)))
                  
                if time.time() > nextPlotTime:
                  nextPlotTime = time.time() + 0.5                                                                        
                  # append to plots
                  y1 = y1[1:]
                  y1 = np.append(y1, voltage) # append voltage
                  line1.set_ydata(y1)
                  
                  y2 = y2[1:]
                  y2 = np.append(y2, current)  # append current
                  line2.set_ydata(y2)
                  
                  y3 = y3[1:]
                  y4 = y4[1:]
                  
                  if POS_CONTROL == True:
                    y3 = np.append(y3, pos) # append position
                    y4 = np.append(y4, set_pos) # append set-pos
                  else:
                    y3 = np.append(y3, rpm) # append rpm 
                    y4 = np.append(y4, set_rpm) # append set-rpm
                  
                  line3.set_ydata(y3)                                        
                  line4.set_ydata(y4)                      
                  
                  fig.canvas.draw()
                  fig.canvas.flush_events()

                time.sleep(0.01)
                
                # Check if there is enough data back for a measurement                
                if ser.in_waiting > 0:                   
                  inbuf += ser.read(ser.in_waiting)                 
                #print(len(inbuf))
                if len(inbuf) > 59:
                  while len(inbuf) > 59:                  
                      (response, consumed) = pyvesc.decode(inbuf)
                      if consumed > 0:                
                          #print("consumed " + str(consumed))                
                          inbuf = inbuf[consumed:]
                          # Print out the values
                          try:                                                
                              #print("response " + str(response.id))                             
                              if isinstance(response, GetFirmwareVersion):                                
                                print("Firmware: " + str(response.version_major) + ", " + str(response.version_minor))
                              elif isinstance(response, GetConfig):                                                            
                                dump(response)
                              elif isinstance(response, GetRotorPosition):                                                                                            
                                pos = response.rotor_pos                                
                                #print("pos: " + str(pos))
                              elif isinstance(response, GetRotorPositionCumulative):
                                pos = response.rotor_pos                                
                                print("pos_cum: " + str(pos))
                              elif isinstance(response, GetValues):
                                rpm = response.rpm
                                voltage = response.input_voltage
                                current = response.avg_motor_current
                                # tacho: one rotation = (pole_counts * 3) 
                                print("pos: " + str(pos) + " T: " + str(response.temp_fet_filtered) + " rpm: "+  str(response.rpm) + " volt: " + str(response.input_voltage) + " curr: " +str(response.avg_motor_current) + " Tachometer:" + str(response.tachometer_value) + " Tachometer ABS:" + str(response.tachometer_abs_value) + " Duty:" + str(response.duty_cycle_now) + " Watt Hours:" + str(response.watt_hours) + " Watt Hours Charged:" + str(response.watt_hours_charged) + " amp Hours:" + str(response.amp_hours) + " amp Hours Charged:" + str(response.amp_hours_charged) + " avg input current:" + str(response.avg_input_current) )
                              elif isinstance(response, GetPrint):                                
                                print("FW>> " + response.msg)
                              else:
                                print("not yet implemented: " + str(response.__class__))
                                
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

    

