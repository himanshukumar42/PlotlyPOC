from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

url = "https://github.com/JaziDesigns/Datasets/raw/main/all_data.csv"
df = pd.read_csv(url)


def dash_render_table(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    app.layout = html.Div([
        html.H1("Life Expectancy by Country", style={"text-align": 'center'}),

        dash_table.DataTable(data=df.to_dict('records'), page_size=20),
    ])
    return app.server


def dash_relationship(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    app.layout = html.Div([
        html.Br(),
        "X-Axis", dcc.Dropdown(id="x_axis", options=[{"label": "Year", "value": "Year"}, {"label": "GDP", "value": "GDP"}],
                               value="Year", clearable=False),
        "Y-Axis", dcc.Dropdown(id="y_axis", options=[{"label": "Year", "value": "Year"}, {"label": "GDP", "value": "GDP"}],
                               value="GDP", clearable=False),
        dcc.Graph(id="scatter")
    ])

    def create_scatter_chart(x_axis="Year", y_axis="GDP"):
        return px.scatter(data_frame=df, x=x_axis, y=y_axis, height=600)

    @callback(Output("scatter", "figure"), [Input("x_axis", "value"), Input("y_axis", "value")])
    def update_scatter_chart(x_axis, y_axis):
        return create_scatter_chart(x_axis, y_axis)

    return app.server


def dash_histogram(flask_app, path):
    print(df.columns)
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )
    app.layout = html.Div([
        html.Br(),
        html.P("Select Column: "),
        dcc.Dropdown(id="dist_column", options=["Life expectancy at birth (years)", "GDP"]),
        dcc.Graph(id="histogram")
    ])

    @app.callback(Output('histogram', 'figure'), [Input('dist_column', 'value')])
    def update_histogram(dist_column="GDP"):
        return px.histogram(data_frame=df, x=dist_column, height=600)

    return app.server


def dash_plots(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    app.layout = html.Div([
        html.H1("Life Expectancy by Country", style={"text-align": 'center'}),
        dcc.Dropdown(
            id='analysis-dropdown',
            options=[
                {'label': 'Life Expectancy', 'value': 'Life expectancy at birth (years)'},
                {'label': 'GDP', 'value': 'GDP'},
            ],
            value='Life expectancy at birth (years)',
            style={'width': '50%', 'margin': '20px auto'}
        ),

        dcc.Graph(id='line-chart', style={'width': '50%'}),
        dcc.Graph(id='scatter-plot'),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='box-plot'),
        dcc.Graph(id='choropleth-map'),
        dcc.Graph(id="sunburst-chart"),
    ])

    @app.callback(
        Output('line-chart', 'figure'),
        [Input('analysis-dropdown', 'value')]
    )
    def update_line_chart(selected_parameter):
        fig = px.line(df, x='Year', y=selected_parameter, color='Country', title=f'{selected_parameter} Over Time')
        return fig

    @app.callback(
        Output('scatter-plot', 'figure'),
        [Input('analysis-dropdown', 'value')]
    )
    def update_scatter_plot(selected_parameter):
        fig = px.scatter(df, x='Life expectancy at birth (years)', y='GDP', color='Country',
                         title=f'Scatter Plot ({selected_parameter} vs GDP)')
        return fig

    @app.callback(
        Output('bar-chart', 'figure'),
        [Input('analysis-dropdown', 'value')]
    )
    def update_bar_chart(selected_parameter):
        avg_life_expectancy = df.groupby('Country')[selected_parameter].mean().reset_index()
        fig = px.bar(avg_life_expectancy, x='Country', y=selected_parameter,
                     title=f'Average {selected_parameter} by Country')
        return fig

    @app.callback(
        Output('box-plot', 'figure'),
        [Input('analysis-dropdown', 'value')]
    )
    def update_box_plot(selected_parameter):
        fig = px.box(df, x='Country', y='GDP', title=f'Distribution of GDP by Country')
        return fig

    @app.callback(
        Output('choropleth-map', 'figure'),
        [Input('analysis-dropdown', 'value')]
    )
    def update_choropleth_map(selected_parameter):
        fig = px.choropleth(df, locations='Country', locationmode='country names', color=selected_parameter,
                            title=f'Choropleth Map of {selected_parameter}')
        return fig

    @app.callback(
        Output('sunburst-chart', 'figure'),
        [Input('analysis-dropdown', 'value')]
    )
    def update_sunburst_chart(selected_parameter):
        fig = px.sunburst(df, path=['Country', 'Year'], values=selected_parameter,
                          title=f'Sunburst Chart of {selected_parameter}')
        return fig

    return app.server
