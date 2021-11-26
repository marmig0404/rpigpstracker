#!/usr/bin/env python
import time
import serial
import re

def get_serial():
        serial.Serial(
                        port='/dev/ttyS0',
                        baudrate = 9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        bytesize=serial.EIGHTBITS,
                        timeout=2
                )

def get_readable(serial_payload):
        if "$GPGGA" in serial_payload:
                                readable_time = time.strftime("%d%m%y %H:%M:%S", localtime)
                                split_payload = re.split(',',serial_payload)
                                lat = '{:.7f}'.format(float(split_payload[2])/100) + " " + split_payload[3]
                                long = '{:.7f}'.format(float(split_payload[4])/100) + " " + split_payload[5] 
                                return '{0} GPS: {1}, {2}'.format(readable_time, lat,long)

def write_to_file(file, line):
        pass

def initialize():

        save_file = open(, "a")
        return(ser,save_file)

def run():
        (ser,file) = initalize()

        while 1:
                ser = get_serial()

                while 1:
                        try:
                                localtime = time.localtime(time.time())
                                serial_payload = ser.readline()
                                print get_readable(serial_payload)
                                write_to_file()
                        except serial.serialutil.SerialException:
                                print "Serial Exception!"
                                break;
                        except ValueError:
                                break;


run()
