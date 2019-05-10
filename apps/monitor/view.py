from flask import request, render_template, jsonify, session
from app import socketio
from models import Equipment, User
from flask_socketio import join_room
from datetime import datetime

# 回调
def callback(flag):
    print(flag)
    return flag

def monitorPage():
    user_id = session.get('id')
    equipments = User.query.filter(User.id == user_id).first().group.equipments
    data = {
        'base':{
            'pageTitle': '监控-云安服务',
            'pageNow': '设备监控',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'username': session.get('username')
        },
        'equipments': [
            {
                'name': e.name,
                'status': e.status,
                'use_department': e.use_department,
                'location': e.location,
                'id': e.id,
                'equipment_class': '消防',
                'info_class': '正常',
                'datetime': datetime.now()
            }
            for e in equipments
        ]
    }
    return render_template('monitor.html', **data) 

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
    code = request.form.get('code')
    dateTime = request.form.get('datetime')
    codeDict = {
        '000': '注册',
        '001': '正常',
        '101': '设备故障',
        '102': '报警'
    }
    socketio.emit(
        'report', 
        {
            'code': code, 
            'describe': codeDict[code],
            'reporter': eid,
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
