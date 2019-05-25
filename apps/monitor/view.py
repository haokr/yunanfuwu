from flask import request, render_template, jsonify, session
from app import socketio
from models import Equipment, User, Alarm_record, Equipment_report_log
from flask_socketio import join_room
from datetime import datetime
from db import db
import time


def callback(flag):
    '''
        回调
    :param flag:
    :return:
    '''
    print(flag)
    return flag


def monitorPage():
    '''
        连接前后端中设备连接信息
        通过web展示其中信息
    :return: 监控设备信息
    '''
    user_id = session.get('id')
    equipments = User.query.filter(User.id == user_id).first().group.equipments
    data = {
        'base': {
            'pageTitle': '监控-云安服务',
            'pageNow': '设备监控',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'username': session.get('username'),
            'userid': session.get('id')
        },
        'equipments': [
            {
                'name': e.name,
                'status': e.status,
                'use_department': e.use_department,
                'location': e.location,
                'id': e.id,
                'gaode_longitude': e.gaode_longitude,
                'gaode_latitude': e.gaode_latitude,
                'equipment_class': '消防',
                'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            }
            for e in equipments
        ]
    }
    return render_template('monitor/monitor.html', **data) 


def connect():
    '''
        通过用户ID获取用户的设备
        用户没有设备返回无设备提示信息
        用户有设备返回添加
    :return: 设备连接状态
    '''
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
    '''
        接收设备提交的信息
        通过设备提交的信息判断状态
    :param eid: 设备ID
    :return:设备状态
    '''
    code = request.form.get('code')
    dateTime = request.form.get('datetime')
    codeDict = {
        '000': '注册',
        '001': '正常',
        '101': '故障',
        '102': '报警'
    }

    class_ = codeDict.get(code, None)
    class_ = class_ if class_ else code

    print(code[0], class_)

    # 日志
    if code[0] == '0':
        try:
            reportData = {
                'equipment_id': eid,
                'class_': class_,
                'report_time': datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
            }
            report = Equipment_report_log(**reportData)
            db.session.add(report)
            db.session.commit()
        except Exception as e:
            print(e)
    # 报警
    elif code[0] == '1':
        try:
            # 报警
            alarmData = {
                'equipment_id': eid,
                'class_': class_,
                'alarm_time': datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
            }
            alarm = Alarm_record(**alarmData)
            # 日志
            reportData = {
                'equipment_id': eid,
                'class_': class_,
                'report_time': datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
            }
            report = Equipment_report_log(**reportData)
            db.session.add(report)
            db.session.add(alarm)

            db.session.commit()
        except Exception as e:
            print(e)

    socketio.emit(
        'report', 
        {
            'code': code, 
            'describe': class_,
            'reporter': eid,
            'datetime': dateTime
        }, 
        room=eid,
        callback=callback
    )
    return 'fine'


def joinRoom(eid):
    '''
        加入 websock room
        根据设备加入每个设备的组
    :param eid: 设备ID
    :return:
    '''
    join_room(eid, sid=session.get('sid'), namespace='/')
    socketio.emit('jump', {'data': 'OK', 'joiner': session.get('username')}, room=eid)
    return 'Hello {} is joined'.format(session.get('username'))
