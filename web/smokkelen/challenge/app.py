from flask import Flask, render_template, request, copy_current_request_context, Response
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from flask_restful import Resource, Api
import string


app = Flask(__name__)
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flag')
def flag():
    data = {'flag' : 'IngeHack{d03s_v4rn1sh_s3cur3_w3bs0ck3t_c0nn3ct10ns?}'}
    return data

@socketio.event
def my_event(message):
    for val in message.values():
        if "FLAG" in val.upper():
            emit('my_response', {'data': 'no flags for you 😂'})  
        else:
            emit('my_response', {'data': message['data']})

@socketio.event
def my_broadcast_event(message):
    for val in message.values():
        if "FLAG" in val.upper():
            emit('my_response', {'data': 'Hmm 🤔'}, broacast=True)  
        else:
            emit('my_response', {'data': message['data']}, broacast=True)

@socketio.event
def join(message):
    join_room(message['room'])
    emit('my_response', {'data': 'In rooms: ' + ', '.join(rooms())})

@socketio.event
def leave(message):
    leave_room(message['room'])
    emit('my_response', {'data': 'In rooms: ' + ', '.join(rooms())})

@socketio.on('close_room')
def on_close_room(message):
    emit('my_response', {'data': 'Room ' + message['room'] + ' is closing.'}, to=message['room'])
    close_room(message['room'])

@socketio.event
def my_room_event(message):
    for val in message.values():
        if "FLAG" in val.upper():
            emit('my_response', {'data': '🥲🥲🥲🥲🥲🥲'}, to=message['room'])  
        else:
            emit('my_response', {'data': message['data']}, to=message['room'])

@socketio.event
def disconnect_request():
    @copy_current_request_context
    def can_disconnect():
        disconnect()
    emit('my_response',
         {'data': 'Disconnected!' }, callback=can_disconnect)

@socketio.event
def my_ping():
    emit('my_pong', {'data': 'ping-pong'})


@socketio.event
def connect():
    emit('my_response', {'data': 'Hi, welcome to Smokklen! Go ahead and send me a message. 😄 btw try to access the flag at localhost:5000/flag'})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)