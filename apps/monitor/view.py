import time
from datetime import datetime

from flask import request, render_template, jsonify, session
from flask_socketio import join_room

from db import db, redis_cli
from models import Equipment, User, Alarm_record, UI_report_log, Data_record
from socketIO import socketio


def monitorPage():
    '''
        连接前后端中设备连接信息
        通过web展示其中信息
    :return: 监控设备信息
    '''
    user_id = session.get('id')
    child_id = request.args.get("child")
    equipments = None 
    if not child_id:
        equipments = User.query.filter(User.id == user_id).first().group.equipments
    else:
        equipments = User.query.filter(User.id == child_id).first().group.equipments
    children = User.query.filter(User.parent_id == user_id, User.live == True).all()

    data = {
        'base': {
            'pageTitle': '监控-云安服务',
            'pageNow': '设备监控',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id'),
            'children': [
                {
                    'id': c.id,
                    'name': c.name
                }
                for c in children
            ],
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
                'datetime': e.data_records.order_by(Data_record.record_time.desc()).first().record_time if e.data_records.first() else "",
                'realTimeData': e.data_records.order_by(Data_record.record_time.desc()).first().data if e.data_records.first() else ""
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
    children = User.query.filter(User.parent_id == user_id, User.live == True).all()

    data = {
        'base': {
            'pageTitle': '监控-云安服务',
            'pageNow': '电气监控',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id'),
            'children': [
                {
                    'id': c.id,
                    'name': c.name
                }
                for c in children
            ],
        }
    }
    return render_template('monitor/electrical.html', **data)


def reportPage():
    '''
    TODO 手动报警页面
    :return:
    '''
    user_id = session.get('id')
    child_id = request.args.get('child', None)
    user_id = child_id if child_id and child_id != 'None' else user_id
    children = User.query.filter(User.parent_id == user_id, User.live == True).all()

    equipments = User.query.filter(User.id == user_id).first().group.equipments
    data = {
        'base': {
            'pageTitle': '设备信息-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '设备信息',
            'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id'),
            'children': [
                {
                    'id': c.id,
                    'name': c.name
                }
                for c in children
            ],
        },
        'child': child_id,
        'equipments': [
            {
                'id': e.id,
                'name': e.name,
                'class_': e.class_,
                'location': e.location,
                'use_department': e.use_department
            }
            for e in equipments if e.live
        ]
    }
    return render_template('monitor/sendReport.html', **data)


def reportPageOnPhone():
    '''
    TODO 手机报警页面
    :return:
    '''
    eid = request.args.get('eid', None)
    e = Equipment.query.filter(Equipment.id == eid).first()
    data = {
        'equipment':
            {
                'id': e.id,
                'name': e.name,
                'class_': e.class_,
                'status': e.status,
                'model': e.model,
                'contact': e.admin.contact,
                'contact_tel': e.admin.contact_tel,
                'use_department': e.use_department
            }
    }
    return render_template('monitor/sendReportOnPhone.html', **data)



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
    realTimeData = request.form.get("realTimeData", "")
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
            return jsonify({
                "msg": "Please enter ip of equipment."
            })
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

    data_record = Data_record(**{
        "equipment_id": eid,
        "class_": codeDict.get(code, "正常"),
        "data": realTimeData,
        "record_time": datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
    })
    db.session.add(data_record)
    db.session.commit()

    # 正常
    if code[0] == '0':
        try:
            isAlarm = redis_cli.get(eid)
            isAlarm = isAlarm.decode() if isAlarm else None
            if isAlarm:
                alarmId = isAlarm.split(",")[0]

                equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
                equipment.status = '正常'
                alarmRecord = Alarm_record.query.filter(Alarm_record.id == alarmId).first()
                alarmRecord.end_time = datetime.now()
                db.session.commit()
                redis_cli.delete(eid)

        except Exception as e:
            raise e
    # 报警
    elif code[0] == '1':
        try:
            # 报警
            isAlarm = redis_cli.get(eid)
            isAlarm = isAlarm.decode() if isAlarm else None
            oldAlarmClass = isAlarm.split(",")[1] if isAlarm else None
            alarmId = isAlarm.split(",")[0] if isAlarm else None

            if not isAlarm:
                equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
                equipment.status = class_
                alarmData = {
                    'equipment_id': eid,
                    'class_': class_,
                    'alarm_time': datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
                }
                alarm = Alarm_record(**alarmData)
                emailMsg = f"警报！ 设备报警！\n 设备id：{eid}\n 设备名称：{equipment.name}\n 设备位置：{equipment.location}\n 所属部门：{equipment.use_department}\n 报警时间：{alarmData['alarm_time']}\n 请及时检查！"
                all_alert(equipment.admin, msg=emailMsg, subject="警报！设备报警！请及时查看！")

                db.session.add(alarm)
                db.session.flush()
                redis_cli.set(eid, f"{alarm.id},{class_}")
                db.session.commit()
            elif oldAlarmClass != class_:
                equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
                equipment.status = class_
                # 将原来的报警结束
                alarmRecord = Alarm_record.query.filter(Alarm_record.id == alarmId).first()
                alarmRecord.end_time = datetime.now()
                redis_cli.delete(eid)
                # 添加新的报警
                alarmData = {
                    'equipment_id': eid,
                    'class_': class_,
                    'alarm_time': datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
                }
                alarm = Alarm_record(**alarmData)
                emailMsg = f"警报！ 设备报警！\n 设备id：{eid}\n 设备名称：{equipment.name}\n 设备位置：{equipment.location}\n 所属部门：{equipment.use_department}\n 报警时间：{alarmData['alarm_time']}\n 请及时检查！"
                all_alert(equipment.admin, msg=emailMsg, subject="警报！设备报警！请及时查看！")

                db.session.add(alarm)
                db.session.flush()
                redis_cli.set(eid, f"{alarm.id},{class_}")
                db.session.commit()
        except Exception as e:
            raise e

    socketio.emit(
        'report',
        {
            'code': code,
            'describe': class_,
            'reporter': eid,
            'datetime': dateTime,
            'readTimeData': realTimeData
        },
        room=eid
    )
    return 'fine'


def UIReport(eid):
    '''
        电压电流报警
    '''
    code = request.form.get('code')
    dateTime = request.form.get('datetime')

    HighPositiveActiveTotalElectricEnergy = request.form.get('HighPositiveActiveTotalElectricEnergy')
    HighPositiveTotalReactivePower = request.form.get('HighPositiveTotalReactivePower')

    AphaseVoltage = request.form.get('AphaseVoltage')
    BphaseVoltage = request.form.get('BphaseVoltage')
    CphaseVoltage = request.form.get('CphaseVoltage')

    AphaseCurrent = request.form.get('AphaseCurrent')
    BphaseCurrent = request.form.get('BphaseCurrent')
    CphaseCurrent = request.form.get('CphaseCurrent')

    TotalActivePowerHigh = request.form.get('TotalActivePowerHigh')
    AphaseActivePower = request.form.get('AphaseActivePower')
    BphaseActivePower = request.form.get('BphaseActivePower')
    CphaseActivePower = request.form.get('CphaseActivePower')

    data = {
        'HighPositiveActiveTotalElectricEnergy': HighPositiveActiveTotalElectricEnergy,
        'HighPositiveTotalReactivePower': HighPositiveTotalReactivePower,

        'AphaseVoltage': AphaseVoltage,
        'BphaseVoltage': BphaseVoltage,
        'CphaseVoltage': CphaseVoltage,

        'AphaseCurrent': AphaseCurrent,
        'BphaseCurrent': BphaseCurrent,
        'CphaseCurrent': CphaseCurrent,

        'TotalActivePowerHigh': TotalActivePowerHigh,
        'AphaseActivePower': AphaseActivePower,
        'BphaseActivePower': BphaseActivePower,
        'CphaseActivePower': CphaseActivePower,
    }

    codeDict = {
        '000': '注册',
        '001': '正常',
        '101': '故障',
        '102': '电压报警',
        '103': '电流报警'
    }
    if code == '000':
        equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
        ip = request.form.get('ip')
        if not (ip and equipment):
            return jsonify({
                "msg": "Please enter ip."
            })
        try:
            equipment.ip = ip
            equipment.status = '正常'
            db.session.commit()
        except Exception as e:
            print(e)
            return 'error when commit db'
        return jsonify({
            "msg": "success"
        })

    class_ = codeDict.get(code, None)
    class_ = class_ if class_ else code

    # 日志
    if code[0] == '0':
        try:
            isAlarm = redis_cli.get(eid)
            isAlarm = isAlarm.decode() if isAlarm else None
            if isAlarm:
                alarmId = isAlarm.split(",")[0]
                equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
                equipment.status = '正常'
                alarmRecord = Alarm_record.query.filter(Alarm_record.id == alarmId).first()
                alarmRecord.end_time = datetime.now()
                db.session.commit()

            data["equipment_id"] = eid
            data["class_"] = class_
            data["report_time"] = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')

            report = UI_report_log(**data)
            db.session.add(report)
            db.session.commit()
            redis_cli.delete(eid)
        except Exception as e:
            print(e)
    # 报警
    elif code[0] == '1':
        try:
            # 报警
            isAlarm = redis_cli.get(eid)
            isAlarm = isAlarm.decode() if isAlarm else None
            oldAlarmClass = isAlarm.split(",")[1] if isAlarm else None
            alarmId = isAlarm.split(",")[0] if isAlarm else None

            if not isAlarm:
                equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
                equipment.status = class_
                db.session.commit()
                emailMsg = f"警报！ 设备报警！\n 设备id：{eid}\n 设备名称：{equipment.name}\n 设备位置：{equipment.location}\n 所属部门：{equipment.use_department}\n 报警时间：{datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')}\n 请及时检查！"
                all_alert(equipment.admin, msg=emailMsg, subject="警报！设备报警！请及时查看！")

            elif oldAlarmClass != class_:
                equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
                equipment.status = class_
                # 将原来的报警结束
                alarmRecord = Alarm_record.query.filter(Alarm_record.id == alarmId).first()
                alarmRecord.end_time = datetime.now()
                redis_cli.delete(eid)
                db.session.commit()
                emailMsg = f"警报！ 设备报警！\n 设备id：{eid}\n 设备名称：{equipment.name}\n 设备位置：{equipment.location}\n 所属部门：{equipment.use_department}\n 报警时间：{datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')}\n 请及时检查！"
                all_alert(equipment.admin, msg=emailMsg, subject="警报！设备报警！请及时查看！")

            alarmData = {
                'equipment_id': eid,
                'class_': class_,
                'alarm_time': datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')
            }



            alarm = Alarm_record(**alarmData)
            # 日志
            data["equipment_id"] = eid
            data["class_"] = class_
            data["report_time"] = datetime.strptime(dateTime, '%Y-%m-%d %H:%M:%S')

            report = UI_report_log(**data)

            db.session.add(alarm)
            db.session.add(report)
            db.session.flush()
            redis_cli.set(eid, f"{alarm.id},{class_}")
            db.session.commit()
        except Exception as e:
            raise e

    socketio.emit(
        'report',
        {
            'code': code,
            'describe': class_,
            'reporter': eid,
            'datetime': dateTime,
        },
        room=eid,
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


def wx_showEquipments():
    '''
        查询当前用户拥有的设备
        获取设备信息
        设备信息展示
    :return: 设备信息
    '''
    user_id = session.get('id')
    child_id = request.args.get('child', None)
    user_id = child_id if child_id and child_id != 'None' else user_id
    equipments = User.query.filter(User.id == user_id).first().group.equipments
    data = {
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
                'contact': e.admin.contact,
                'contact_tel': e.admin.contact_tel,
                'status': e.status,
                'SIM_id': e.SIM_id,
                'modify_time': e.modify_time,
                'create_time': e.create_time
            }
            for e in equipments if e.live
        ]
    }
    return jsonify(data)


# 给用户及其父账号发送邮件
def all_alert(user, msg, subject=None):
    stack = [user.email]
    while True:
        if user.parent:
            stack.append(user.parent.email)
            user = user.parent
        else:
            break
    for email in stack:
        if email:
            send_mail(msg_to=email, content=msg, subject=subject)


# 发送邮件(qq.com)

import smtplib
from email.mime.text import MIMEText


def send_mail(msg_from=None, passwd=None, msg_to=None, subject=None, content=None):
    # 发送者的邮箱
    msg_from = '3312447390@qq.com'
    # 发送者邮箱的权限码
    passwd = 'vqbzsgcmezrvchfd'
    # 接收的邮箱
    if not msg_to:
        return False

    # 标题
    if not subject:
        subject = "设备警告"
    # 内容
    if not content:
        content = "有紧急事故"
    # 生成一个MIMEText对象（还有一些其他参数）
    msg = MIMEText(content)
    # 放入邮件主题
    msg['Subject'] = subject
    # 放入发件人
    msg['From'] = msg_from

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        return True
    except s.SMTPException as e:
        print(e)
    finally:
        s.quit()
