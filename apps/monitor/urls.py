from flask import Blueprint, request, session
from flask_socketio import send, emit
from socketIO import socketio
from apps.monitor import view

monitor = Blueprint('monitor', __name__) 

@monitor.route('/')
def monitorPage():
    return view.monitorPage()

@monitor.route('/report/<eid>', methods=['POST'])
def report(eid):
    return view.report(eid)

@socketio.on('connect')
def connect():
    return view.connect()

@monitor.route('/join/<eid>', methods=['POST'])
def join(eid):
    return view.joinRoom(eid)

