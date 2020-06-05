from flask import request, session, jsonify, render_template, url_for, redirect
from models import User, Group, Equipment, Role
from db import db

from socket import socket, AF_INET, SOCK_STREAM
import time
import requests


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
    return render_template('equipment/equipments.html', **data)


def showEditEquipment(eid):
    '''
        通过设备ID查询设备信息
        设备信息修改并存储
    :param eid: 设备ID
    :return:
    '''
    user_id = session.get("id")
    e = Equipment.query.filter(Equipment.id == eid, Equipment.live == True).first()
    children = User.query.filter(User.parent_id == user_id, User.live == True).all()
    data = {
        'base':{
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
        'equipment': {
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
            'heartbeat_interval': e.heartbeat_interval,
            'position_province': e.position_province,
            'position_city': e.position_city,
            'position_district': e.position_district,
            'create_time': e.create_time,
            'status': e.status,
            'SIM_id': e.SIM_id,
            'modify_time': e.modify_time
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
    children = User.query.filter(User.parent_id == user_id, User.live == True).all()
    if role.if_add_equipment == False:
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
                'status': e.status,
                'SIM_id': e.SIM_id,
                'modify_time': e.modify_time
                }
                for e in equipments if e.live
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
            'child': child_id
        }
        return render_template('equipment/addEquipment.html', **data)


def controlPage():
    user_id = session.get('id')
    eid = request.args.get('eid', None)

    if not eid:
        return 'error parm'

    children = User.query.filter(User.parent_id == user_id, User.live == True).all()
    data = {
        'base': {
            'pageTitle': '设备反控-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '设备反控',
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
        'eid': eid
    }
    return render_template('equipment/control.html', **data)

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
    class_ = request.form.get('class_')
    use_department = request.form.get('use_department')
    location = request.form.get('location')
    gaode_location = request.form.get('gaode_location')
    manufacturer = request.form.get('manufacturer')
    model = request.form.get('model')
    SIM_id = request.form.get("SIM_id")
    remarks = request.form.get('remarks')

    gaode_longitude, gaode_latitude = [ float(x) for x in gaode_location.split(',')]

    cityData = requests.get('https://restapi.amap.com/v3/geocode/regeo?output=json&location={}&key=1f5f34e6c96735e4be689afb6ec22a82&radius=10&extensions=base'.format(gaode_location)).json()


    position_province = cityData['regeocode']['addressComponent']['province']
    position_city = cityData['regeocode']['addressComponent']['city']
    position_district = cityData['regeocode']['addressComponent']['district']

    position_province = position_province if position_province else None
    position_city = position_city if position_city else None
    position_district = position_district if position_district else None

    equipmentInfo = {
        'name': name,
        'use_department': use_department,
        'location': location,
        'gaode_latitude': gaode_latitude,
        'gaode_longitude': gaode_longitude,
        'class_': class_,
        'manufacturer': manufacturer,
        'model': model,
        'remarks': remarks,
        'SIM_id': SIM_id,
        'admin': user,
        'position_province': position_province,
        'position_city': position_city,
        'position_district': position_district
    }

    if equipmentInfo['class_'] == '电气':
        equipmentInfo['id'] = 'e_' + str(int(time.time()))

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
            equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True)
            equipment.update({key: value})
            db.session.commit()
            return jsonify({'msg': 'success', 'data': 'modify equipment success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'data': 'modify equipment error when select equipments'})

def drop():
    eid = request.form.get('eid', None)
    if not eid:
        return jsonify({'msg': 'fail', 'data': 'parm error'})

    equipment = Equipment.query.filter(Equipment.id == eid, Equipment.live == True)

    if not equipment:
        return jsonify({'msg': 'fail', 'data': 'not the equipment'})

    try:
        equipment.update({"live": False})
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'data': 'db commit error'})
    return jsonify({'msg': 'success', 'data': 'success'})



def control(eid):
    option = request.form.get('option')
    switch = request.form.get('switch')

    if not ( switch and option ):
        return jsonify({'msg': 'fail', 'data': 'parm error'})

    equipment = Equipment.query.filter(Equipment.id == eid).first()
    if not equipment:
        return jsonify({'msg': 'fail', 'data': 'not the equipment'})

    ip = equipment.ip


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

    # 服务器的ip地址
    address='127.0.0.1'   
    # 服务器的端口号
    port = 8020           
    # 接收数据的缓存大小
    buffsize = 1024        

    s = socket(AF_INET, SOCK_STREAM) 
    s.connect((address, port))

    s.send(senddata.encode())
    s.close()
    return jsonify({'msg': 'success', 'data': 'success'})


def getUserEquipments():
    '''
    TODO 获取用户的设备
    :param id:
    :return:
    '''
    user_id = session.get('id')
    equipments = User.query.filter(User.id == user_id).first().group.equipments
    data = [
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
    return jsonify(data)

def getHeartbeat(eid):
    equipment = Equipment.query.filter(Equipment.id == eid).first()

    if not equipment:
        return jsonify({
            "msg": "fail, Without this equipment."
        })

    return jsonify({
        "msg": "success",
        "data": equipment.heartbeat_interval
    })