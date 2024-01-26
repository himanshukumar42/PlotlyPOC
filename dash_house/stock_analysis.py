import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Sample dataset (replace this with your actual dataset)
data = {
    'SquareFeet': [1400, 1600, 1700, 1875, 1100, 1550, 2350, 2450, 1425, 1700],
    'Price': [245000, 312000, 279000, 308000, 199000, 219000, 405000, 324000, 319000, 255000]
}

df = pd.DataFrame(data)

# Feature and target
X = df[['SquareFeet']]
y = df['Price']

# Linear regression model
model = LinearRegression()
model.fit(X, y)

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='House Price Prediction'),

    html.Div(children='''
        Enter the square footage to get the predicted price:
    '''),

    dcc.Input(id='square-feet-input', type='number', value=1500),

    html.Div(id='predicted-price-output'),

    dcc.Graph(
        id='scatter-plot',
        figure=px.scatter(df, x='SquareFeet', y='Price', trendline='ols', title='Scatter Plot with Regression Line')
    ),

    dcc.Graph(
        id='histogram',
        figure=px.histogram(df, x='Price', nbins=10, title='Price Distribution')
    ),

    dcc.Graph(
        id='residuals-plot',
        figure=px.scatter(x=X.squeeze(), y=model.predict(X) - y, title='Residuals Plot')
    ),
])

# Callback to update predicted price
@app.callback(
    Output('predicted-price-output', 'children'),
    [Input('square-feet-input', 'value')]
)
def update_predicted_price(square_feet):
    predicted_price = model.predict([[square_feet]])[0]
    return f'Predicted Price: ${predicted_price:.2f}'

if __name__ == '__main__':
    app.run_server(debug=True)
