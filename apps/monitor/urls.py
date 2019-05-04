from flask import Blueprint, request, session
from flask_socketio import send, emit
from socketIO import socketio
from apps.monitor import view

monitor = Blueprint('monitor', __name__) 

@monitor.route('/')
def monitorPage():
    return view.monitorPage()

@monitor.route('/jump', methods=['POST'])
def jump():
    return view.sendJump()

@monitor.route('/report/<eid>', methods=['POST'])
def report(eid):
    return view.report(eid)


@socketio.on('connect')
def connect():
    sid = request.sid
    session['sid'] = sid
    socketio.emit(
        'start',
        {'data': 'server connect success', 'sid': sid},
        room=sid
    )
