from flask import request, render_template, jsonify, session
from app import socketio
from models import Equipment, User
from flask_socketio import join_room

# 回调
def callback(flag):
    print(flag)
    return flag

def monitorPage():
    return render_template('monitor.html') 

def connect():
    sid = request.sid
    session['sid'] = sid
    uid = session.get('id')
    user = User.query.filter(User.id == uid).first()
    if not user:
        return {'msg': 'fail', 'data': 'Not the user'}
    usersEquipments = user.group.equipments
    if not usersEquipments:
        return {'msg': 'success', 'data': 'Havent equipment in this user'}
    for e in usersEquipments:
        join_room(e.id, sid=sid, namespace='/')
        socketio.emit(
            'join', 
            {'data': 'OK', 'joiner': session.get('username')}, 
            room=e.id,
            callback=callback
        )
    return {'msg': 'success', 'data': 'OK, The user {} has joined equipments room'.format(session.get('username'))}

def report(eid):
    reportData = request.form.get('data')
    dateTime = request.form.get('datetime')
    socketio.emit(
        'jump', 
        {
            'data': reportData, 
            'reporter': session.get('username'),
            'datetime': dateTime
        }, 
        room=eid,
        callback=callback
    )
    return 'fine'

def joinRoom(eid):
    join_room(eid, sid=session.get('sid'), namespace='/')
    socketio.emit('jump', {'data': 'OK', 'joiner': session.get('username')}, room=eid)
    return 'Hello {} is joined'.format(session.get('username'))
