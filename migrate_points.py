from functools import reduce
import sqlite3
import re
import operator

import pynmea2
import pandas as pd

con = sqlite3.connect('locations.db')
cur = con.cursor()


def checksum(nmea_str):
    return reduce(operator.xor, map(ord, nmea_str), 0)


def read_db():
    ex_str = "SELECT * FROM prod"
    cur.execute(ex_str)
    rows = cur.fetchall()
    for row in rows:
        print(row)
        lat = float('.' + re.sub("\D", "", row[2]))*10000
        norsou = row[2][-1]
        long = float('.' + re.sub("\D", "", row[3]))*10000
        easwes = row[3][-1]
        payload = "GPGGA,100216.00,{0},{1},{2},{3},1,09,0.96,224.0,M,-35.1,M,,".format(
            '{:.5f}'.format(lat), norsou, '{:.5f}'.format(long), easwes)
        payload = '$' + payload + '*' + (hex(checksum(payload))[2:])
        write_to_db(row[1], row[0], payload)


def write_to_db(date_time, epoch, serial_payload):
    try:
        parsed_payload = pynmea2.parse(serial_payload, check=False)

        lat = parsed_payload.latitude
        long = parsed_payload.longitude
        execution_string = "INSERT INTO migrate VALUES ({0},datetime('now','localtime'),\"{1}\",\"{2}\")".format(
            epoch, '{:.8f}'.format(lat), '{:.8f}'.format(long))
        try:
            # print(execution_string)
            cur.execute(execution_string)
        except sqlite3.OperationalError:
            cur.execute(
                "CREATE TABLE migrate(epoch numeric, datetime date, latitude text, longitude text)")
            cur.execute(execution_string)
        con.commit()
    except (KeyError, AttributeError, pynmea2.ParseError):
        pass


read_db()
cur.execute('DELETE FROM prod WHERE true')
cur.execute('INSERT INTO prod SELECT * FROM migrate')
cur.execute('DROP TABLE migrate')
con.commit()
