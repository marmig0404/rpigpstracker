import sqlite3
import math


def gen_circle(total, current):
    x = math.cos(2*math.pi * (current/total))
    y = math.sin(2*math.pi * (current/total))
    long = ('{:.8f}'.format(x) +
            'E') if x >= 0 else ('{:.8f}'.format(-1*x) + 'W')
    lat = ('{:.8f}'.format(y) + 'N') if y >= 0 else ('{:.8f}'.format(-1*y) + 'S')
    return (long, lat)


con = sqlite3.connect('locations.db')
cur = con.cursor()

num_rows = 2000

#cur.execute("CREATE TABLE testing(epoch numeric, datetime date, latitude text, longitude text)")
for cur_row in range(num_rows):
    epoch = cur_row
    (long, lat) = gen_circle(num_rows, cur_row)
    execution_string = "INSERT INTO testing VALUES ({0},datetime('now','localtime'),\"{1}\",\"{2}\")".format(
        epoch, lat, long)
    print(str(long) + "," + str(lat))
    cur.execute(execution_string)
    con.commit()

con.close()
