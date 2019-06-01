from flask import request, session, render_template, redirect, url_for, jsonify
from models import User, Group, Role
from db import db
import time
import json


def getRoles():
    '''
        显示登陆用户创建的所有角色
    :return:
    '''
    user_id = session.get('id')
    user = User.query.filter(User.id == user_id).first()
    role = Role.query.filter(Role.id == user.role_id).first()
    if role.if_role == False:
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
                    'status': e.status,
                    'SIM_id': e.SIM_id,
                    'modify_time': e.modify_time,
                    'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                }
                for e in equipments
            ]
        }
        return render_template('monitor/monitor.html', **data)
    else:
        create_user = user_id
        all_roles = Role.query.filter(Role.create_user == create_user).all()
        data = {
            'base': {
                'pageTitle': '监控-云安服务',
                'pageNow': '设备监控',
                'avatarImgUrl': '/static/img/yunan_logo_1.png',
                'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id')
            },
            'roles': [
                {
                    'id': e.id,
                    'name': e.name,
                    'remarks': e.remarks,
                    'if_role': e.if_role,
                    'if_add_equipment': e.if_add_equipment,
                    'if_modify_equipment': e.if_modify_equipment,
                    'if_add_child': e.if_add_child,
                    'if_modify_child': e.if_modify_child,
                    'create_time': e.create_time,
                    'modify_time': e.modify_time
                }
                for e in all_roles
            ]
        }
        return render_template('roles/roles.html', **data)


def showRole(rid):
    '''
        展示角色信息
    :return:
    '''
    user_id = session.get('id')
    user = User.query.filter(User.id == user_id).first()
    role = Role.query.filter(Role.id == user.role_id).first()
    if role.if_role == False:
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
                    'status': e.status,
                    'SIM_id': e.SIM_id,
                    'modify_time': e.modify_time,
                    'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                }
                for e in equipments
            ]
        }
        return render_template('monitor/monitor.html', **data)
    else:
        role = Role.query.filter(Role.id == rid, Role.create_user ==user_id).first()
        userlist = User.query.filter(User.role_id == rid).all()
        others = User.query.filter(User.parent_id == user_id, User.role_id != role.id).all()
        data = {
            'base': {
                'pageTitle': '设备信息-云安服务',
                'avatarImgUrl': '/static/img/yunan_logo_1.png',
                'pageNow': '用户信息',
                'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id')
            },
            'role': {
                    'id': role.id,
                    'name': role.name,
                    'username': user.username,
                    'if_role': role.if_role,
                    'if_add_equipment': role.if_add_equipment,
                    'if_modify_equipment': role.if_modify_equipment,
                    'if_drop_equipment': role.if_drop_equipment,
                    'if_add_child': role.if_add_child,
                    'if_modify_child': role.if_modify_child,
                    'if_drop_child': role.if_drop_child,
                    'create_time': role.create_time,
                    'modify_time': role.modify_time
                },
            'user': [
                {
                    'id': c.id,
                    'name': c.name,
                    'username': c.username,
                    'address': c.address,
                    'contact': c.contact,
                    'contact_tel': c.contact_tel,
                    'create_time': c.create_time,
                    'modify_time': c.modify_time
                }
                for c in userlist
            ],
            'others': [
                {
                    'id': a.id,
                    'name': a.name,
                    'username': a.username,
                    'address': a.address,
                    'contact': a.contact,
                    'contact_tel': a.contact_tel,
                    'create_time': a.create_time,
                    'modify_time': a.modify_time
                }
                for a in others
            ]
        }
        return render_template('roles/exitRoles.html', **data)


def modifyRole(rid):
    '''
        获取用户提交要修改的角色信息
        修改角色信息并存储
    :param uid: 用户ID
    :return: 设备信息修改状态
    '''
    user_id = session.get('id')
    user = User.query.filter(User.id == user_id).first()
    role = Role.query.filter(Role.id == user.role_id).first()
    if role.if_role == False:
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
                    'status': e.status,
                    'SIM_id': e.SIM_id,
                    'modify_time': e.modify_time,
                    'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                }
                for e in equipments
            ]
        }
        return render_template('monitor/monitor.html', **data)
    else:
        key = request.form.get('key')
        value = request.form.get('value')
        if value == '':
            value = None
        elif value == '是':
            value = True
        elif value == '否':
            value = False
        try:
            role = Role.query.filter(Role.id == rid)
            role.update({key: value})
            user.modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            db.session.commit()
            return jsonify({'msg': 'success', 'data': 'modify equipment success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'data': 'modify equipment error when select equipments'})


def Roleadd():
    '''
    新增角色
    :return:
    '''
    user_id = session.get('id')
    name = request.form.get('name')
    remarks = request.form.get('remarks')
    if_role = request.form.get('if_role')
    if if_role == 'false':
        if_role = False
    else:
        if_role = True
    if_add_equipment = request.form.get('if_add_equipment')
    if if_add_equipment == 'false':
        if_add_equipment = False
    else:
        if_add_equipment = True
    if_modify_equipment = request.form.get('if_modify_equipment')
    if if_modify_equipment == 'false':
        if_modify_equipment = False
    else:
        if_modify_equipment = True
    if_drop_equipment = request.form.get('if_modify_equipment')
    if if_drop_equipment == 'false':
        if_drop_equipment = False
    else:
        if_drop_equipment = True
    if_add_child = request.form.get('if_add_child')
    if if_add_child == 'false':
        if_add_child = False
    else:
        if_add_child = True
    if_modify_child = request.form.get('if_modify_child')
    if if_modify_child == 'false':
        if_modify_child = False
    else:
        if_modify_child = True
    if_drop_child = request.form.get('if_modify_equipment')
    if if_drop_child == 'false':
        if_drop_child = False
    else:
        if_drop_child = True
    roleInfo = {
        'name': name,
        'remarks': remarks,
        'create_user': user_id,
        'if_role': if_role,
        'if_add_equipment': if_add_equipment,
        'if_modify_equipment': if_modify_equipment,
        'if_drop_equipment': if_drop_equipment,
        'if_add_child': if_add_child,
        'if_modify_child': if_modify_child,
        'if_drop_child': if_drop_child
    }
    try:
        role = Role(**roleInfo)
        db.session.add(role)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'data': 'add equipment error when commit database'})
    return jsonify({'msg': 'success', 'data': 'add success'})


def addRole(rid):
    '''
        添加使用角色的用户
    :param rid:
    :return:
    '''
    userlist = request.form.get('userlist')
    userlist = json.loads(userlist)
    try:
        for u in userlist:
            user = User.query.filter(User.id == u).first()
            user.role_id = rid
            db.session.commit()
        return jsonify({'msg': 'success', 'data': 'modify user s role success'})
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'data': 'modify user s role fails'})


def showaddRole():
    '''
        展示角色添加页面
    :return:
    '''
    user_id = session.get('id')
    user = User.query.filter(User.id == user_id).first()
    role = Role.query.filter(Role.id == user.role_id).first()
    if role.if_role == False:
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
            'name': session.get('name'),
            'userid': session.get('id')
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
                for e in equipments
            ]
        }
        return render_template('equipment/equipments.html', **data)
    else:
        data = {
            'base': {
                'pageTitle': '添加设备-云安服务',
                'avatarImgUrl': '/static/img/yunan_logo_1.png',
                'pageNow': '添加设备',
                'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id')
            }
        }
        return render_template('roles/addRoles.html', **data)