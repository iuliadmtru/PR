from flask import Flask, render_template, url_for, redirect, request
from markupsafe import Markup
from plotly.offline import plot
from plotly.graph_objs import Scatter, Marker

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/results', methods=['GET', 'POST'])
def results():
    if request.method == 'GET':
        my_plot_div = plot([Scatter(x=['Jan 1'], y=[3], marker=Marker(size=10, color='blue')),
                            Scatter(x=['Jan 2'], y=[4], marker=Marker(size=10, color='blue')),
                            Scatter(x=['Jan 3'], y=[6], marker=Marker(size=10, color='red')),
                            Scatter(x=['Jan 4'], y=[5], marker=Marker(size=10, color='green')),
                            Scatter(x=['Jan 5'], y=[5], marker=Marker(size=10, color='green')),
                            ],
                            output_type='div')
        return render_template('results.html', div_placeholder=Markup(my_plot_div))
    elif request.method == 'POST':
        return redirect(url_for('static'))  ## TODO: add button
