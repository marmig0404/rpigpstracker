import sqlite3

import pandas as pd
import plotly.express as px


def generate_new_point_plot(plot_name, dark_mode=False):
    try:
        execution_string = "SELECT * FROM prod"
        print("Generating new plot from query: \n\t" + execution_string)
        con = sqlite3.connect('locations.db')
        df = pd.read_sql_query(execution_string, con)

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
            autotypenumbers='convert types',
            showlegend=False,
            coloraxis_showscale=False
        )
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
        fig.write_html(plot_name+".html", include_plotlyjs='cdn',
                       include_mathjax='cdn')
        print("Wrote plot to {0}.html".format(plot_name))
    except ValueError:
        print("No values in db to plot.")


def generate_new_geo_plot(plot_name):
    try:
        px.set_mapbox_access_token(open(".mapbox_token").read())
    except FileNotFoundError:
        print("Create '.mapbox_token' and populate to use geo plotting.")

    execution_string = "SELECT * FROM prod"
    print("Generating new geo plot from query: \n\t" + execution_string)
    con = sqlite3.connect('locations.db')
    df = pd.read_sql_query(execution_string, con)

    df['latitude'] = pd.to_numeric(df['latitude'])
    df['longitude'] = pd.to_numeric(df['longitude'])

    df = df[df['latitude'] != 0]
    df = df[df['longitude'] != 0]

    fig = px.line_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        hover_name='datetime',
    )
    fig.update_layout(
        coloraxis_showscale=False,
    )
    fig.write_html(plot_name+".html", include_plotlyjs='cdn',
                   include_mathjax='cdn')
    print("Wrote plot to {0}.html".format(plot_name))
