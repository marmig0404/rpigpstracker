import plotly.express as px
import sqlite3

con = sqlite3.connect('locations.db')
cur = con.cursor()

execution_string = "SELECT * FROM dev"
epochs = []
datetimes = []
lats = []
longs = []
for epoch, datetime, lat, long in cur.execute(execution_string):
    epochs.append(epoch)
    datetimes.append(datetime)
    lat_number = float(lat[-len(lat)])
    lats.append(float(lat[-len(lat)])
                if "N" in lat else -1*float(lat[-len(lat)]))
    longs.append(float(long[-len(long)])
                 if "E" in long else -1*float(long[-len(long)]))

fig = px.scatter(x=longs, y=lats, color=epochs,
                 label=datetimes, template="simple_white")
fig.write_html("plot.html")
