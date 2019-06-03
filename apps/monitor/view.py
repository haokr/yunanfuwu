from flask import request, render_template, jsonify, session
from app import socketio
from models import Equipment, User, Alarm_record, Equipment_report_log, UI_report_log
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
            'name': session.get('name'),
            'userid': session.get('id')
        },
        'equipments': [
            {
            'id': e.id,
            'name': e.name,
            'class_': e.class_,
            'gaode_longitude': e.gaode_longitude,
            'gaode_latitude': e.gaode_latitude,
            'location': e.location,
            'ip': e.ip,
            'use_department': e.use_department,
            'remarks': e.remarks,
            'manufacturer': e.manufacturer,
            'model': e.model,
            'position_province': e.position_province,
            'position_city': e.position_city,
            'position_district': e.position_district,
            'create_time': e.create_time,
            'contact': e.admin.contact,
            'contact_tel': e.admin.contact_tel,
            'status': e.status,
            'SIM_id': e.SIM_id,
            'modify_time': e.modify_time,
            'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            }
            for e in equipments if e.live == True
        ]
    }
    return render_template('monitor/monitor.html', **data) 

def electricalMonitorPage():
    '''
        连接前后端中设备连接信息
        通过web展示其中信息
    :return: 监控设备信息
    '''
    user_id = session.get('id')

    data = {
        'base': {
            'pageTitle': '监控-云安服务',
            'pageNow': '电气监控',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id')
        }
    }
    return render_template('monitor/electrical.html', **data) 


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

    if code == '000':
        equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
        ip = request.form.get('ip')
        if not (ip and equipment):
            return 'fail, zhuce mei you ip'
        try:    
            equipment.ip = ip
            equipment.status = '正常'
            db.session.commit()
        except Exception as e:
            print(e)
            return 'error when commit db'    
        return 'regist success'

    class_ = codeDict.get(code, None)
    class_ = class_ if class_ else code
    try:
        equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
        equipment.status = class_
        db.session.commit()
    except Exception as e:
        print(e)

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

def UIReport(eid):
    '''
        电压电流报警
    '''
    code = request.form.get('code')
    dateTime = request.form.get('datetime')
    data = request.form.get('data')

    codeDict = {
        '000': '注册',
        '001': '正常',
        '101': '故障',
        '102': '电压报警',
        '103': '电流报警',
        '104': '漏电报警',
        '105': '温度报警'
    }
    if code == '000':
        equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
        ip = request.form.get('ip')
        if not (ip and equipment):
            return 'fail, zhuce mei you ip'
        try:    
            equipment.ip = ip
            equipment.status = '正常'
            db.session.commit()
        except Exception as e:
            print(e)
            return 'error when commit db'    
        return 'regist success'

    class_ = codeDict.get(code, None)
    class_ = class_ if class_ else code

    try:    
        equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
        equipment.status = class_
        db.session.commit()
    except Exception as e:
        print(e)

    # 日志
    if code[0] == '0':
        try:
            reportData = {
                'equipment_id': eid,
                'class_': class_,
                'describe': data['describe'],
                # 电压
                'U1': data['U1'],
                'U2': data['U2'],
                'U3': data['U3'],
                # 电流
                'I1': data['I1'],
                'I2': data['I2'],
                'I3': data['I3'],
                # 设备用电
                'J1': data['J1'],
                # 温度
                'T1': data['T1'],
                'T2': data['T2'],
                'T3': data['T3'],
                'T4': data['T4'],
                # 剩余电流，漏电
                'L1': data['L1'],

                'report_time': datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
            }
            report = UI_report_log(**reportData)
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
                'describe': data['describe'],
                'alarm_time': datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
            }
            alarm = Alarm_record(**alarmData)
            # 日志
            reportData = {
                'equipment_id': eid,
                'class_': class_,
                'describe': data['describe'],
                # 电压
                'U1': data['U1'],
                'U2': data['U2'],
                'U3': data['U3'],
                # 电流
                'I1': data['I1'],
                'I2': data['I2'],
                'I3': data['I3'],
                # 设备用电
                'J1': data['J1'],
                # 温度
                'T1': data['T1'],
                'T2': data['T2'],
                'T3': data['T3'],
                'T4': data['T4'],
                # 剩余电流，漏电
                'L1': data['L1'],

                'report_time': datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
            }
            report = UI_report_log(**reportData)

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
            'datetime': dateTime,
            'data': data
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
