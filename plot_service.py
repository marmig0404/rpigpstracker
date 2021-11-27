import re
import sqlite3

import plotly.express as px


def generate_new_plot(plot_name):
    print("Plot Serivce starting, connecting to db...")
    con = sqlite3.connect('locations.db')
    cur = con.cursor()

    execution_string = "SELECT * FROM prod"
    print("Generating new plot from query: \n" + execution_string)
    epochs = []
    datetimes = []
    lats = []
    longs = []
    for epoch, datetime, lat, long in cur.execute(execution_string):
        epochs.append(epoch)
        datetimes.append(datetime)
        digit_lat = float(re.sub('\D', '', lat))
        parsed_lat = float(digit_lat if "N" in lat else -1*digit_lat)
        lats.append(parsed_lat)
        digit_long = float(re.sub('\D', '', long))
        parsed_long = digit_long if "E" in long else -1*digit_long
        longs.append(parsed_long)
    fig = px.scatter(x=longs, y=lats, color=epochs,
                     hover_name=datetimes, template="ggplot2", title='GPS Data', labels={'x': '', 'y': ''})
    fig.update_layout(coloraxis_showscale=False)
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    fig.write_html(plot_name+".html")
    print("Wrote plot to {0}.html".format(plot_name))
