import sqlite3
import time

import serial
import pynmea2

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


def write_to_db(serial_payload):
    if "$GPGGA" in serial_payload:
        parsed_payload = pynmea2.parse(serial_payload)

        lat = parsed_payload.latitude
        long = parsed_payload.longitude
        epoch = '{:.0f}'.format(time.time())

        execution_string = "INSERT INTO prod VALUES ({0},datetime('now','localtime'),\"{1}\",\"{2}\")".format(
            epoch, lat, long)
        try:
            cur.execute(execution_string)
        except sqlite3.OperationalError:
            cur.execute(
                "CREATE TABLE prod(epoch numeric, datetime date, latitude text, longitude text)")
            cur.execute(execution_string)
        con.commit()


def run():
    while 1:
        ser = get_serial()
        while 1:
            try:
                serial_payload = ser.readline()
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
