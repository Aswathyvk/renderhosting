from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit
from collections import defaultdict

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# In-memory message store (can be replaced with database)
rooms_messages = defaultdict(list)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('chat', {'msg': f'{username} has joined the room.'}, room=room)

    # Send old messages to the new user
    for msg in rooms_messages[room]:
        emit('chat', msg)

@socketio.on('message')
def handle_message(data):
    room = data['room']
    msg = {'msg': f"{data['username']}: {data['message']}"}
    rooms_messages[room].append(msg)
    emit('chat', msg, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)

