import plotly.express as px
from dash.dependencies import Input, Output
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import pandas_datareader.data as web
import datetime

start = datetime.datetime(2020, 1, 1)
end = datetime.datetime(2023, 11, 11)

stock = 'AAPL'

df = web.DataReader(stock, 'yahoo', start=start, end=end)


def stock_plots(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )
    app.layout = html.Div([
        html.H1("Stock Analysis", style={'text-align': 'center'}),

        html.Div(children='''
            Dash: Application with Flask
        '''),
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': df.index, 'y': df.Close, 'type': 'line', 'name': stock},
                ],
                'layout': {
                    'title': stock,
                }
            }
        )
    ])

    @app.callback(
        Output('new-life-exp', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_strip_chart(selected_parameter):
        fig = px.strip(df, x="lifeExp")
        return fig

    return app.server
