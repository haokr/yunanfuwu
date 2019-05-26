from flask import request, session, jsonify, render_template, url_for, redirect
from models import User, Group, Equipment, Role
from db import db

from socket import socket, AF_INET, SOCK_STREAM
import time


'''
    Page
'''

def getEquipments():
    '''
        设备信息获取
    :return:
    '''
    return redirect('/monitor')


def showEquipments():
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
        'base':{
            'pageTitle': '设备信息-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '设备信息',
            'username': session.get('username'),
            'userid': session.get('id')
        },
        'child': child_id,
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
                'id': e.id,
                'SIM_id': e.SIM_id
            }
            for e in equipments
        ]
    }
    return render_template('equipment/equipments.html', **data)


def showEditEquipment(eid):
    '''
        通过设备ID查询设备信息
        设备信息修改并存储
    :param eid: 设备ID
    :return:
    '''
    e = Equipment.query.filter(Equipment.id == eid).first()
    data = {
        'base': {
            'pageTitle': '设备信息-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '设备信息',
            'username': session.get('username'),
            'userid': session.get('id')
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
    return render_template('equipment/editEquipment.html', **data)


def showAddEquipment():
    '''
        新增设备展示
    :return:
    '''
    user_id = session.get('id')
    user = User.query.filter(User.id == user_id).first()
    role = Role.query.filter(Role.id == user.role_id).first()
    if role.if_add_equipment == False:
        user_id = session.get('id')
        child_id = request.args.get('child', None)
        user_id = child_id if child_id and child_id != 'None' else user_id

        equipments = User.query.filter(User.id == user_id).first().group.equipments
        data = {
            'base': {
                'pageTitle': '设备信息-云安服务',
                'avatarImgUrl': '/static/img/yunan_logo_1.png',
                'pageNow': '设备信息',
                'username': session.get('username'),
                'userid': session.get('id')
            },
            'child': child_id,
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
                    'id': e.id,
                    'SIM_id': e.SIM_id
                }
                for e in equipments
            ]
        }
        return render_template('equipment/equipments.html', **data)
    else:
        child_id = request.args.get('child', None)
        data = {
            'base':{
                'pageTitle': '添加设备-云安服务',
                'avatarImgUrl': '/static/img/yunan_logo_1.png',
                'pageNow': '添加设备',
                'username': session.get('username'),
                'userid': session.get('id')
            },
            'child': child_id
        }
        return render_template('equipment/addEquipment.html', **data)


'''
    API
'''


def addEquipment():
    '''
        新增设备
        将新设备添加至数据库
    :return: 数据添加结果
    '''
    child = request.args.get('child', None)
    user_id = child if child and child != 'None' else session.get('id')

    if not user_id:
        return jsonify({'msg': 'fail', 'data': 'please to login'})
    user = User.query.filter(User.id == user_id).first()

    name = request.form.get('name')
    use_department = request.form.get('use_department')
    location = request.form.get('location')
    ip = request.form.get('ip')
    gaode_latitude = request.form.get('gaode_latitude')
    gaode_longitude = request.form.get('gaode_longitude')
    manufacturer = request.form.get('manufacturer')
    model = request.form.get('model')
    remarks = request.form.get('remarks')

    equipmentInfo = {
        'name': name,
        'use_department': use_department,
        'location': location,
        'ip': ip,
        'gaode_latitude': gaode_latitude,
        'gaode_longitude': gaode_longitude,
        'class_': '消防',
        'manufacturer': manufacturer,
        'model': model,
        'remarks': remarks,
        'admin': user
    }

    try:
        equipment = Equipment(**equipmentInfo)
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


def modifyEquipment(eid):
    '''
        获取用户提交要修改的设备信息
        修改设备信息并存储
    :param eid: 用户ID
    :return: 设备信息修改状态
    '''
    user_id = session.get('id')
    user = User.query.filter(User.id == user_id).first()
    role = Role.query.filter(Role.id == user.role_id).first()
    if role.if_modify_equipment == False:
        return jsonify({'msg': 'fail', 'data': 'do not have role'})
    else:
        key = request.form.get('key')
        value = request.form.get('value')
        if value == '':
            value = None
        try:
            equipment = Equipment.query.filter(Equipment.id == eid)
            equipment.update({key: value})
            db.session.commit()
            return jsonify({'msg': 'success', 'data': 'modify equipment success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'data': 'modify equipment error when select equipments'})


def control(eid):
    switch = request.form.get('switch')
    option = request.form.get('option')

    if not (switch and option):
        return jsonify({'msg': 'fail', 'data': 'parm error'})

    equipment = Equipment.query.filter(Equipment.id == eid).first()
    if not equipment:
        return jsonify({'msg': 'fail', 'data': 'not the equipment'})

    ip = equipment.ip


    # 服务器的ip地址
    address='127.0.0.1'   
    # 服务器的端口号
    port = 8020           
    # 接收数据的缓存大小
    buffsize = 1024        

    s = socket(AF_INET, SOCK_STREAM) 
    s.connect((address, port))

    instructions = {
        '0': {
            'on': 'relay0_on',
            'off': 'relay0_off',
            },
        '1': {
            'on': 'relay1_on',
            'off': 'relay1_off',
            },
        '2': {
            'on': 'relay2_on',
            'off': 'relay2_off',
            },
        '3': {
            'on': 'relay3_on',
            'off': 'relay3_off'
            }
    }

    senddata = '{}:{}'.format(ip, instructions[switch][option])
    s.send(senddata.encode())
    s.close()
    return jsonify({'msg': 'success', 'data': 'success'})

