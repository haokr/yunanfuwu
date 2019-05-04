from flask import request, render_template, jsonify, session
from app import socketio


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