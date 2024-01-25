import plotly.express as px
from dash.dependencies import Input, Output
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

df = px.data.gapminder().query("year == 2007")


def new_plots(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )
    app.layout = html.Div([
        html.H1("New Life Expectancy", style={'text-align': 'center'}),
        dcc.Graph('new-life-exp')
    ])

    @app.callback(
        Output('new-life-exp', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_strip_chart(selected_parameter):
        fig = px.strip(df, x="lifeExp")
        return fig

    return app.server
