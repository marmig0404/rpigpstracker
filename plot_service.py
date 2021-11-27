import re
import sqlite3

import plotly.express as px


def generate_new_plot(plot_name):
    print("Plot Serivce starting, connecting to db...")
    con = sqlite3.connect('locations.db')
    cur = con.cursor()

    execution_string = "SELECT * FROM prod ORDER BY epoch desc"
    print("Generating new plot from query: \n" + execution_string)
    epochs, datetimes, latitudes, longitudes = ([], ) * 4
    for epoch, datetime, latitude, longitude in cur.execute(execution_string):
        epochs.append(epoch)
        datetimes.append(datetime)
        digit_latitude = float(re.sub('\D', '', latitude))
        parsed_latitude = digit_latitude if "N" in latitude else -1*digit_latitude
        latitudes.append(parsed_latitude)
        digit_longitude = float(re.sub('\D', '', longitude))
        parsed_longitude = digit_longitude if "E" in longitude else -1*digit_longitude
        longitudes.append(parsed_longitude)
    fig = px.scatter(x=longitudes,
                     y=latitudes,
                     color=epochs,
                     hover_name=datetimes,
                     template="ggplot2",
                     title='GPS Data',
                     labels={'x': '', 'y': ''}
                     )
    fig.update_layout(showlegend=False,
                      coloraxis_showscale=False
                      )
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )
    fig.write_html(plot_name+".html")
    print("Wrote plot to {0}.html".format(plot_name))
