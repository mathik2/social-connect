from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

# Use asyncio mode (no eventlet/gevent required)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="asyncio")

@app.route('/')
def index():
    return render_template('index.html')

# Relay WebRTC offer
@socketio.on('offer')
async def handle_offer(data):
    await emit('offer', data, broadcast=True, include_self=False)

# Relay WebRTC answer
@socketio.on('answer')
async def handle_answer(data):
    await emit('answer', data, broadcast=True, include_self=False)

# Relay ICE candidates
@socketio.on('ice-candidate')
async def handle_ice_candidate(data):
    await emit('ice-candidate', data, broadcast=True, include_self=False)

# Relay hangup
@socketio.on('hangup')
async def handle_hangup():
    await emit('hangup', broadcast=True, include_self=False)

if __name__ == '__main__':
    # For local testing, fallback to Flask dev server
    socketio.run(app, host='0.0.0.0', port=5000)
