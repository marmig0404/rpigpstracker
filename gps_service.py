import datetime
import re
import sqlite3
import time
from os import read
import serial

con = sqlite3.connect('locations.db')
cur = con.cursor()


def get_serial():
    while 1:
        try:
            return serial.Serial(
                port='/dev/ttyS0',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=2
            )
        except serial.serialutil.SerialException:
            print("Serial Exception!")
            break


def print_coords(serial_payload):
    if "$GPGGA" in serial_payload:
        localtime = time.localtime(time.time())
        readable_time = time.strftime("%d%m%y %H:%M:%S", localtime)
        split_payload = re.split(',', serial_payload)
        lat = '{:.8f}'.format(
            float(split_payload[2])/100) + " " + split_payload[3]
        long = '{:.8f}'.format(
            float(split_payload[4])/100) + " " + split_payload[5]
        print('{0} GPS: {1}, {2}'.format(readable_time, lat, long))


def write_to_save(save_name, serial_payload):
    if "$GPGGA" in serial_payload:
        save_file = open("save/" + save_name, "a")
        split_payload = re.split(',', serial_payload)
        lat = '{:.8f}'.format(
            float(split_payload[2])/100) + "," + split_payload[3]
        long = '{:.8f}'.format(
            float(split_payload[4])/100) + "," + split_payload[5]
        localtime = time.localtime(time.time())
        readable_time = time.strftime("%d%m%y %H:%M:%S", localtime)
        epoch = '{:.0f}'.format(time.time())
        line = "{0},{1},{2},{3}".format(epoch, readable_time, lat, long) + '\n'
        save_file.write(line)
        save_file.close()


def write_to_db(serial_payload):
    if "$GPGGA" in serial_payload:
        split_payload = re.split(',', serial_payload)
        lat = '{:.8f}'.format(
            float(split_payload[2])/100) + split_payload[3]
        long = '{:.8f}'.format(
            float(split_payload[4])/100) + split_payload[5]
        epoch = '{:.0f}'.format(time.time())
        execution_string = "INSERT INTO prod VALUES ({0},datetime('now'),\"{1}\",\"{2}\")".format(
            epoch, lat, long)
        #print("DB Execute: " + execution_string)
        try:
            cur.execute(execution_string)
            con.commit()
        except sqlite3.OperationalError:
            cur.execute(
                "CREATE TABLE prod(epoch numeric, datetime date, latitude text, longitude text)")
            cur.execute(execution_string)
            con.commit()


def run():
    # localtime = time.localtime(time.time())
    # save_name = "GPS-Save-" + \
    #     time.strftime("%d%m%y-%H%M%S", localtime) + ".csv"
    # print('Writing to ' + save_name)
    while 1:
        ser = get_serial()
        while 1:
            try:
                serial_payload = ser.readline()
                # print_coords(serial_payload)
                #write_to_save(save_name, serial_payload)
                write_to_db(serial_payload)
                time.sleep(0.1)
            except serial.serialutil.SerialException:
                print("Serial Exception!")
                break
            except ValueError:
                break
            except KeyboardInterrupt:
                con.close()
                print("Done.")
                exit()


run()
