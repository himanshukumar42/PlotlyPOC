from flask import Flask, render_template
from dash_app.dash_app_plots import dash_plots, dash_histogram, dash_render_table
from dash_app.mytest import life_expectancy
from dash_app.country import new_plots

server = Flask(__name__)  # Flask server
# functions having the dash applications

dash_plots(server, path='/plots/')
life_expectancy(server, path='/hello/')
new_plots(server, path='/test/')
dash_render_table(server, path='/table/')
dash_histogram(server, path='/histogram/')


@server.route('/')  # home page renders the 'index.html'
def index():
    """Render index.html."""
    return render_template('index.html')


if __name__ == '__main__':
    server.run(port=5002)
