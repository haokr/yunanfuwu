from flask import Blueprint, request, session
from flask_socketio import send, emit
from app import socketio
from apps.monitor import view
from . import monitor

@monitor.route('/')
def monitorPage():
    return view.monitorPage()

@monitor.route('/jump', methods=['POST'])
def jump():
    return view.sendJump()

@socketio.on('connect')
def connect():
    sid = request.sid
    session['sid'] = sid
    socketio.emit(
        'start',
        {'data': 'server connect success', 'sid': sid},
        room=sid
    )
