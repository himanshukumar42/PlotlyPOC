from dash import Dash, html, dcc, dash_table, callback
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

url = "https://github.com/JaziDesigns/Datasets/raw/main/all_data.csv"
df = pd.read_csv(url)

columns = df.columns.tolist()


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


def create_scatter_chart(x_axis="Year", y_axis="GDP"):
    global df
    return px.scatter(data_frame=df, x=x_axis, y=y_axis)


def dash_relationship(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    x_axis = dcc.Dropdown(id="x_axis", options=columns, value="Year", clearable=False)
    y_axis = dcc.Dropdown(id="y_axis", options=columns, value="GDP", clearable=False)

    app.layout = html.Div([
        html.H1(className='main-title', children='Global Life Expectancy'),
        x_axis,
        y_axis,
        dcc.Graph(id="scatterplot")
    ])

    @app.callback(
        Output("scatterplot", "figure"),
        [Input("x_axis", "value"), Input("y_axis", "value")])
    def update_scatter_chart(x_axis="Year", y_axis="GDP"):
        print("******************* HORRAY ************")
        return create_scatter_chart(x_axis, y_axis)

    return app.server


def dash_histogram(flask_app, path):
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
        print("******************* HORRAY Histogram************")

        return px.histogram(data_frame=df, x=dist_column, height=600)

    return app.server


def dash_plots(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    # app.layout = html.Div([
    #     html.H1(className='main-title', children='Global Life Expectancy'),
    #     html.Div([
    #         html.H3(
    #             className='subtitle',
    #             children='Scatter Plot between the Life Expectancy and GDP'
    #         ),
    #         html.Div([
    #             html.Div([
    #                 html.H4(
    #                     children='Flow',
    #                     style={
    #                         'font-size': '1.2vw',
    #                         'text-align': 'center',}
    #                 ),
    #                 dcc.Dropdown(
    #                     id='analysis-dropdown',
    #                     options=[
    #                         {'label': 'Life Expectancy', 'value': 'Life expectancy at birth (years)'},
    #                         {'label': 'GDP', 'value': 'GDP'},
    #                     ],
    #                     value='Life expectancy at birth (years)',
    #                     style={'width': '130px', 'display': 'inline-block', 'margin-top': '2%', 'z-index': '1'}
    #                 ),
    #             ], className='dropdowns-container'),
    #             html.Div([
    #                 dcc.Graph(id='line-chart'),
    #             ])
    #         ]),
    #         html.Div([
    #             dcc.Link(
    #                 dbc.Button(
    #                     "To main Page",
    #                     className="button-text"),
    #                 href="/",
    #                 refresh=True,
    #                 style={'margin': '2%'}),
    #             dcc.Link(
    #                 dbc.Button(
    #                     "To Histogram",
    #                     className='button-text'),
    #                 href="/histogram/",
    #                 refresh=True,
    #                 style={'margin': '2%'})
    #         ], className='buttons-container')
    #     ]),
    #     html.Div([
    #         dcc.Graph(id='scatter-plot'),
    #         dcc.Graph(id='bar-chart'),
    #         dcc.Graph(id='box-plot'),
    #         dcc.Graph(id='choropleth-map'),
    #         dcc.Graph(id="sunburst-chart"),
    #     ]),
    #     ]),

    app.layout = html.Div([
        html.H1(className='main-title', children='Global Life Expectancy'),
        html.H3(className='subtitle', children='Scatter Plot between the Life Expectancy and GDP'),
        dcc.Dropdown(
            id='analysis-dropdown',
            options=[
                {'label': 'Life Expectancy', 'value': 'Life expectancy at birth (years)'},
                {'label': 'GDP', 'value': 'GDP'},
            ],
            value='Life expectancy at birth (years)',
            style={'width': '130px', 'display': 'inline-block', 'margin-top': '2%', 'z-index': '1'}
        ),
        dcc.Graph(id='line-chart'),
        dcc.Graph(id='scatter-plot'),
        dcc.Graph(id='bar-chart'),
        dcc.Graph(id='box-plot'),
        dcc.Graph(id='choropleth-map'),
        dcc.Graph(id="sunburst-chart"),
        dcc.Link(
            dbc.Button("To main Page", className="button-text"),
            href="/",
            refresh=True,
            style={'margin': '2%'}
        ),
        dcc.Link(
            dbc.Button("To Histogram", className='button-text'),
            href="/histogram/",
            refresh=True,
            style={'margin': '2%'}
        ),

    ])

    @app.callback(
        Output('line-chart', 'figure'),
        [Input('analysis-dropdown', 'value'), ]
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
