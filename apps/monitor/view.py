from flask import request, render_template, jsonify, session
from app import socketio
from models import Equipment
from flask_socketio import join_room

def monitorPage():
    return render_template('monitor.html') 

def sendJump():
    data = request.form.get('data')
    sid = session.get('sid')
    socketio.emit(
        'jump', 
        {'data': data, 'sid': sid},
        room=sid
    )
    return jsonify({'msg': 'success', 'data': data})

def report(eid):
    socketio.emit('jump', {'data': 'OK', 'reporter': session.get('username')}, room=eid)
    return 'fine'

def joinRoom(eid):
    join_room(eid, sid=session.get('sid'), namespace='/')
    socketio.emit('jump', {'data': 'OK', 'joiner': session.get('username')}, room=eid)
    return 'Hello {} is joined'.format(session.get('username'))
