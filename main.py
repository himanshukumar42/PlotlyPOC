from flask import Flask, render_template
from dash_app.dash_app_plots import dash_plots, dash_histogram, dash_render_table, dash_relationship
from dash_app.mytest import life_expectancy
from dash_app.country import new_plots
from dash_house.house_price_prediction import dash_house_table

server = Flask(__name__)

dash_plots(server, path='/plots/')
life_expectancy(server, path='/hello/')
new_plots(server, path='/test/')
dash_render_table(server, path='/table/')
dash_histogram(server, path='/histogram/')
dash_relationship(server, path='/relationships/')
dash_house_table(server, path='/house/')

@server.route('/')
def index():
    return render_template('index.html')

@server.route("/healthz")
def healthz():
    return "Health check"

@server.route("/posit")
def posit():
    return "Posit Connect"

if __name__ == '__main__':
    server.run(host='0.0.0.0', port=80)
