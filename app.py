from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Using default async_mode (gevent) which works on Python 3.13
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

# Relay WebRTC offer
@socketio.on('offer')
def handle_offer(data):
    emit('offer', data, broadcast=True, include_self=False)

# Relay WebRTC answer
@socketio.on('answer')
def handle_answer(data):
    emit('answer', data, broadcast=True, include_self=False)

# Relay ICE candidates
@socketio.on('ice-candidate')
def handle_ice_candidate(data):
    emit('ice-candidate', data, broadcast=True, include_self=False)

# Relay hangup signal
@socketio.on('hangup')
def handle_hangup():
    emit('hangup', broadcast=True, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
