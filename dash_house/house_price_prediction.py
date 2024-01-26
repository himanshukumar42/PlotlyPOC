import os

import pandas as pd
import numpy as np
import seaborn as sns
from dash import Dash, html, dcc, dash_table, callback
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.express as px

house_df = pd.read_csv(f"{os.getcwd()}/data.csv")

X = house_df[['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'waterfront', 'view', 'condition']]
y = house_df['price']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)


def dash_house_table(flask_app, path):
    app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname=path,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
    )

    app.layout = html.Div([
        html.H1("House Price Prediction Database", style={"text-align": 'center'}),
        dash_table.DataTable(data=house_df.to_dict('records'), page_size=20, style_table={'height': '400px', 'overflowY': 'auto', 'margin': '10px'}),
        dcc.Dropdown(
            id='dropdown-columns',
            options=[{'label': col, 'value': col} for col in house_df.select_dtypes('number').columns],
            multi=True,
            value=house_df.select_dtypes('number').columns.tolist()
        ),
        dcc.Graph(id='scatter-matrix-plot'),
        dcc.Graph(id='heatmap'),

        html.Div([
            html.Label('Number of Bedrooms', style={'margin-bottom': '10px'}),
            dcc.Input(id='bedrooms-input', type='number', value=3, style={'margin-bottom': '20px'}),

            html.Label('Number of Bathrooms', style={'margin-bottom': '10px'}),
            dcc.Input(id='bathrooms-input', type='number', value=2, style={'margin-bottom': '20px'}),

            html.Label('Square Footage (Living)', style={'margin-bottom': '10px'}),
            dcc.Input(id='sqft-living-input', type='number', value=1500, style={'margin-bottom': '20px'}),

            html.Label('Square Footage (Lot)', style={'margin-bottom': '10px'}),
            dcc.Input(id='sqft-lot-input', type='number', value=4000, style={'margin-bottom': '20px'}),

            html.Label('Number of Floors', style={'margin-bottom': '10px'}),
            dcc.Input(id='floors-input', type='number', value=1, style={'margin-bottom': '20px'}),

            html.Label('Waterfront (0 for No, 1 for Yes)', style={'margin-bottom': '10px'}),
            dcc.Input(id='waterfront-input', type='number', value=0, style={'margin-bottom': '20px'}),

            html.Label('View (0 for No, 1 for Yes)', style={'margin-bottom': '10px'}),
            dcc.Input(id='view-input', type='number', value=0, style={'margin-bottom': '20px'}),

            html.Label('Condition', style={'margin-bottom': '10px'}),
            dcc.Input(id='condition-input', type='number', value=3, style={'margin-bottom': '20px'}),

            html.Br(),

            html.H1(id='predicted-price-output')
        ], style={'width': '50%', 'margin': 'auto', 'textAlign': 'center'})
    ])

    @app.callback(
        Output('scatter-matrix-plot', 'figure'),
        [Input('dropdown-columns', 'value'),]
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

    @app.callback(
        Output('predicted-price-output', 'children'),
        [Input('bedrooms-input', 'value'),
         Input('bathrooms-input', 'value'),
         Input('sqft-living-input', 'value'),
         Input('sqft-lot-input', 'value'),
         Input('floors-input', 'value'),
         Input('waterfront-input', 'value'),
         Input('view-input', 'value'),
         Input('condition-input', 'value'),]
    )
    def update_predicted_price(bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition):
        print("*********** HOORAY *********")
        predicted_price = model.predict([[bedrooms, bathrooms, sqft_living, sqft_lot, floors, waterfront, view, condition]])[0]
        return f'Predicted Price: ${predicted_price:.2f}'

    return app.server
