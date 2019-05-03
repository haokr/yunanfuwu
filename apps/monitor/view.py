from flask import request, render_template, jsonify
from app import socketio


def monitorPage():
    return render_template('monitor.html') 

def sendJump():
    data = request.form.get('data')
    socketio.emit('jump', data)
    return jsonify({'msg': 'success', 'data': data})