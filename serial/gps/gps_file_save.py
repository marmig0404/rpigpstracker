#!/usr/bin/env python
import time
import serial
import re

def get_serial():
    while 1:
        try:
            return serial.Serial(
                port='/dev/ttyS0',
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=2
                    )
        except serial.serialutil.SerialException:
                print("Serial Exception!")
                break;

def print_coords(serial_payload):
    if "$GPGGA" in serial_payload:
        localtime = time.localtime(time.time())
        readable_time = time.strftime("%d%m%y %H:%M:%S", localtime)
        split_payload = re.split(',',serial_payload)
        lat = '{:.7f}'.format(float(split_payload[2])/100) + " " + split_payload[3]
        long = '{:.7f}'.format(float(split_payload[4])/100) + " " + split_payload[5] 
        print('{0} GPS: {1}, {2}'.format(readable_time, lat,long))

def write_to_save(save_name,serial_payload):
    if "$GPGGA" in serial_payload:
        save_file = open("save/" + save_name, "a")
        split_payload = re.split(',',serial_payload)
        lat = '{:.7f}'.format(float(split_payload[2])/100) + "," + split_payload[3]
        long = '{:.7f}'.format(float(split_payload[4])/100) + "," + split_payload[5]
        localtime = time.localtime(time.time())
        readable_time = time.strftime("%d%m%y %H:%M:%S", localtime)
        epoch = '{:.0f}'.format(time.time())
        line = "{0},{1},{2},{3}".format(epoch,readable_time,lat,long) + '\n'
        save_file.write(line)
        save_file.close()
  
def run():
    localtime = time.localtime(time.time())
    save_name = "GPS-Save-" + time.strftime("%d%m%y-%H%M%S", localtime) + ".csv"
    print('Writing to ' + save_name)
    while 1:
        ser = get_serial()
        while 1:
            try:
                    serial_payload = ser.readline()
                    print_coords(serial_payload)
                    write_to_save(save_name,serial_payload)
            except serial.serialutil.SerialException:
                    print("Serial Exception!")
                    break;
            except ValueError:
                    break;
            except KeyboardInterrupt:
                    print("Done.")
                    exit()

                                


run()
