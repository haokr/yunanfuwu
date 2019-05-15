from flask import request, session, jsonify, render_template, url_for, redirect
from models import User, Group, Equipment
from db import db


# 设备获取
def getEquipments():
    return redirect('/monitor')


# 新增设备方法
def addEquipment():
    name = request.form.get('name')
    user_id = session.get('id')
    if not user_id:
        return jsonify({'msg': 'fail', 'data': 'please to login'})
    user = User.query.filter(User.id == user_id).first()
    try:
        equipment = Equipment(name=name)
        equipment.group.append(user.group)
        while user.parent_id:
            user = user.parent
            equipment.group.append(user.group)
        db.session.add(equipment)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'data': 'add equipment error when commit database'})
    return jsonify({'msg': 'success', 'data': 'add success'})


# 修改设备信息方法
def modifyEquipment(eid):
    key = request.form.get('key')
    value = request.form.get('value')
    if value == '':
        value = None
    try:
        print(key, value)
        equipment = Equipment.query.filter(Equipment.id == eid)
        equipment.update({key: value})
        db.session.commit()
        return jsonify({'msg': 'success', 'data': 'modify equipment success'})
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'data': 'modify equipment error when select equipments'})


# 设备信息展示方法
def showEquipments():
    user_id = session.get('id')
    equipments = User.query.filter(User.id == user_id).first().group.equipments
    data = {
        'base':{
            'pageTitle': '设备信息-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '设备信息',
            'username': session.get('username')
        },
        'equipments': [
            {
                'name': e.name,
                'status': e.status,
                'use_department': e.use_department,
                'location': e.location,
                'remark': e.remarks,
                'manufacturer': e.manufacturer,
                'model': e.model,
                'create_time': e.create_time,
                'id': e.id
            }
            for e in equipments
        ]
    }
    return render_template('equipments.html', **data)


# 设备信息修改方法
def showEditEquipment(eid):
    e = Equipment.query.filter(Equipment.id == eid).first()
    data = {
        'base':{
            'pageTitle': '设备信息-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '设备信息',
            'username': session.get('username')
        },
        'equipment': {
                'name': e.name,
                'status': e.status,
                'use_department': e.use_department,
                'location': e.location,
                'remarks': e.remarks,
                'manufacturer': e.manufacturer,
                'model': e.model,
                'create_time': e.create_time,
                'id': e.id,
                'ip': e.ip,
                'gaode_longitude': e.gaode_longitude,
                'gaode_latitude': e.gaode_latitude
            }
    }
    return render_template('editEquipment.html', **data)


# 新增设备展示方法
def showAddEquipment():
    data = {
        'base':{
            'pageTitle': '添加设备-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '添加设备',
            'username': session.get('username')
        }
    }
    return render_template('addEquipment.html', **data)