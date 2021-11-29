import re
import sqlite3

import pandas as pd
import plotly.express as px


def generate_new_plot(plot_name, dark_mode=False):
    try:
        execution_string = "SELECT * FROM prod"
        print("Generating new plot from query: \n\t" + execution_string)
        con = sqlite3.connect('locations.db')
        df = pd.read_sql_query(execution_string, con)

        def convert_coord_to_number(input):
            try:
                only_num = float(re.sub('N|E|S|W', '', input))
                return only_num if "N" in input or "E" in input else -1*only_num
            except ValueError:
                return 0

        df['longitude'] = df['longitude'].apply(convert_coord_to_number)
        df['latitude'] = df['latitude'].apply(convert_coord_to_number)

        fig = px.scatter(
            data_frame=df,
            x="longitude",
            y="latitude",
            color="epoch",
            hover_name="datetime",
            template=(
                "plotly_dark" if dark_mode else "ggplot2"
            ),
            title='GPS Data'
        )
        fig.update_layout(
            showlegend=False,
            coloraxis_showscale=False
        )
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
        fig.write_html(plot_name+".html")
        print("Wrote plot to {0}.html".format(plot_name))
    except ValueError:
        print("No values in db to plot.")
