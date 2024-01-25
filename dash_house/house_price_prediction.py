import os

import pandas as pd
import numpy as np
import seaborn as sns
from dash import Dash, html, dcc, dash_table, callback
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.express as px

house_df = pd.read_csv(f"{os.getcwd()}/data.csv")


def dash_house_table(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    app.layout = html.Div([
        html.H1("House Price Prediction Database", style={"text-align": 'center'}),
        dash_table.DataTable(data=house_df.to_dict('records'), page_size=20),
        dcc.Dropdown(
            id='dropdown-columns',
            options=[{'label': col, 'value': col} for col in house_df.select_dtypes('number').columns],
            multi=True,
            value=house_df.select_dtypes('number').columns.tolist()
        ),
        dcc.Graph(id='scatter-matrix-plot'),
        dcc.Graph(id='heatmap')
    ])

    @app.callback(
        Output('scatter-matrix-plot', 'figure'),
        [Input('dropdown-columns', 'value')]
    )
    def update_scatter_matrix(selected_columns):
        if not selected_columns:
            return px.scatter()

        fig = px.scatter_matrix(
            house_df,
            dimensions=selected_columns,
            color='price',  # You can change this to another variable if needed
            height=700
        )

        return fig

    @app.callback(
        Output('heatmap', 'figure'),
        [Input('heatmap', 'relayoutData')]
    )
    def update_heatmap(relayoutData):
        numeric_df = house_df.select_dtypes(include=['number'])
        correlation_matrix = numeric_df.corr()

        fig = go.Figure(data=go.Heatmap(
            z=correlation_matrix.values,
            x=correlation_matrix.columns,
            y=correlation_matrix.columns,
            colorscale='Viridis',
        ))

        fig.update_layout(title='Correlation Heatmap')
        return fig

    return app.server
