from time import sleep
from random import randint
from threading import Thread, Event
from flask import render_template, Flask
from flask_socketio import SocketIO


app = Flask(__name__)
sio = SocketIO(app)

line_thread = Thread()
candle_thread = Thread()
thread_stop_event = Event()


# sends a new data point to the client every second
class LineThread(Thread):

    def __init__(self):
        self.delay = 1
        super(LineThread, self).__init__()

    def number_generator(self):
        print("Generating line values")
        while not thread_stop_event.isSet():
            n = randint(-10, 10)
            sio.emit('new_number', {'number': n}, namespace='/line')
            sleep(self.delay)

    def run(self):
        self.number_generator()


# sends a new candle to the client every second
class CandleThread(Thread):

    def __init__(self):
        self.delay = 1
        super(CandleThread, self).__init__()

    def candle_generator(self):
        print("Generating candle values")
        while not thread_stop_event.isSet():
            Open = randint(90, 110)
            High = randint(110, 130)
            Low = randint(70, 90)
            Close = randint(90, 100)
            sio.emit('new_candle', {'candle': [Open, High, Low, Close]}, namespace='/candle')
            sleep(self.delay)

    def run(self):
        self.candle_generator()


@app.route('/')
def index():
    return render_template('index.html')


@sio.on('connect', namespace='/line')
def line_chart():
    global line_thread
    print("Line chart running")
    if not line_thread.isAlive():       # check to make sure the thread isn't already running
        thread = LineThread()
        thread.start()


@sio.on('connect', namespace='/candle')  # run both charts when a client connects
def candle_chart():
    global candle_thread
    print("Candle chart running")
    if not candle_thread.isAlive():
        thread = CandleThread()
        thread.start()


if __name__ == "__main__":
    sio.run(app, host='0.0.0.0')
