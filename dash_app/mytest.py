from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output

df = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')


def life_expectancy(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    placeholder_fig = px.scatter()
    app.layout = html.Div([
        dcc.Graph(
            id='life-exp-vs-gdp',
            figure=placeholder_fig
        ),
        dcc.Interval(
            id='interval-component',
            interval=60 * 1000,  # in milliseconds, update every 1 minute
            n_intervals=0
        )
    ])

    # Define callback to update the figure
    @app.callback(
        Output('life-exp-vs-gdp', 'figure'),
        Input('interval-component', 'n_intervals')
    )
    def update_graph(n_intervals):
        # Update the figure with the latest data
        fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                         size="population", color="continent", hover_name="country",
                         log_x=True, size_max=60)
        return fig

    return app.server
