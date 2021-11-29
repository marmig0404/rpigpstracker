import sqlite3
import math


def gen_circle(total, current):
    long = '{:.8f}'.format(40*math.cos(2*math.pi * (current/total)))
    lat = '{:.8f}'.format(40*math.sin(2*math.pi * (current/total)))
    return (long, lat)


con = sqlite3.connect('locations.db')
cur = con.cursor()

num_rows = 20


try:
    cur.execute("DELETE FROM testing WHERE true")
except sqlite3.OperationalError:
    cur.execute(
        "CREATE TABLE testing(epoch numeric, datetime date, latitude text, longitude text)")

for cur_row in range(num_rows):
    epoch = cur_row
    (long, lat) = gen_circle(num_rows, cur_row)
    execution_string = "INSERT INTO testing VALUES ({0},datetime('now','localtime'),\"{1}\",\"{2}\")".format(
        epoch, lat, long)
    print(str(long) + "," + str(lat))
    cur.execute(execution_string)
    con.commit()

con.close()
