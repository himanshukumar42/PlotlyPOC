from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

data = {
    "Year": [2010, 2011, 2012, 2013, 2014],
    "GDP": [1000, 1200, 900, 1500, 1800],
    "Life Expectancy": [75, 76, 78, 80, 81],
}
df = pd.DataFrame(data)

columns = df.columns.tolist()


def create_scatter_chart(x_axis="Year", y_axis="GDP"):
    return px.scatter(data_frame=df, x=x_axis, y=y_axis, height=600)


x_axis = dcc.Dropdown(id="x_axis", options=columns, value="Year", clearable=False)
y_axis = dcc.Dropdown(id="y_axis", options=columns, value="GDP", clearable=False)

app.layout = html.Div([
    html.H1(className='main-title', children='Global Life Expectancy'),
    "X-Axis", x_axis,
    "Y-Axis", y_axis,
    dcc.Graph(id="scatter")
])


@callback(Output("scatter", "figure"), [Input("x_axis", "value"), Input("y_axis", "value")])
def update_scatter_chart(x_axis, y_axis):
    return create_scatter_chart(x_axis, y_axis)

if __name__ == '__main__':
    app.run(port=5003)
