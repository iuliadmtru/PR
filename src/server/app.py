from datetime import datetime

from flask import Flask, render_template, url_for, redirect, request
from plotly.offline import plot
from plotly.graph_objs import Scatter, Figure, Layout

app = Flask(__name__)

beeps = False
should_beep = False

board_data = []

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/status')
def status():
    return {'beeps': beeps}

@app.get('/graph')
def graph():
    times = [t[0] for t in board_data]
    temps = [t[1] for t in board_data]
    beeps = [int(t[2]) for t in board_data]

    plt = plot(Figure(
        data=[
            Scatter(x=times, y=temps, name='Temperatures', yaxis='y1'),
            Scatter(x=times, y=beeps, name='Beeps', yaxis='y2')
        ],
        layout=Layout(
            title='Temperature and Beeps Over Time',
            xaxis=dict(
                title='Time',
                tickformat='%H:%M:%S',
                type='date'
            ),
            yaxis=dict(
                title='Temperature',
                range=[-5, 105],
            ),
            yaxis2=dict(
                title='Beeps',
                range = [-0.05, 1.05],
                overlaying='y',
                side='right'
            )
        )
    ), output_type='div', include_plotlyjs='cdn')

    return plt

@app.post('/stop')
def stop():
    global beeps, should_beep

    should_beep = False
    beeps = False

    return redirect(url_for('index'))

@app.post('/board')
def board_post():
    global beeps, should_beep, board_data

    beeps = request.json['beeps']
    should_beep_board = request.json['should_beep']
    temp = request.json['temp']

    board_data.append((datetime.now(), temp, beeps))

    if should_beep_board:
        should_beep = True

    return {'should_beep': should_beep}

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'), host="0.0.0.0", port=5001)
    # app.run(host="0.0.0.0", port=5001)