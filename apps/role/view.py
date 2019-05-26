from flask import request, session, render_template, redirect, url_for, jsonify
from models import User, Group, Role
from db import db
import time


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
                'userid': session.get('id')
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
                'userid': session.get('id')
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
                    'datetime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                }
                for e in equipments
            ]
        }
        return render_template('monitor/monitor.html', **data)
    else:
        role = Role.query.filter(Role.id == rid and Role.create_user ==user_id).first()
        userlist = User.query.filter(User.role_id == rid).all()
        other = User.query.filter(User.parent_id == user_id and User.role_id != role.id).all()
        data = {
            'base': {
                'pageTitle': '设备信息-云安服务',
                'avatarImgUrl': '/static/img/yunan_logo_1.png',
                'pageNow': '用户信息',
                'username': session.get('username'),
                'userid': session.get('id')
            },
            'role': {
                    'id': role.id,
                    'name': role.name,
                    'username': user.username,
                    'if_role': role.if_role,
                    'if_add_equipment': role.if_add_equipment,
                    'if_modify_equipment': role.if_modify_equipment,
                    'if_add_child': role.if_add_child,
                    'if_modify_child': role.if_modify_child,
                    'create_time': role.create_time,
                    'modify_time': role.modify_time
                },
            'user': [
                {
                    'id': c.id,
                    'name': c.name,
                    'username': c.username,
                    'parent': c.parent.username,
                    'address': c.address,
                    'contact': c.contact,
                    'contact_tel': c.contact_tel,
                    'create_time': c.create_time,
                    'modify_time': c.modify_time
                }
                for c in userlist
            ],
            'other': [
                {
                    'id': c.id,
                    'name': c.name,
                    'username': c.username,
                    'parent': c.parent.username,
                    'address': c.address,
                    'contact': c.contact,
                    'contact_tel': c.contact_tel,
                    'create_time': c.create_time,
                    'modify_time': c.modify_time
                }
                for c in other
            ]
        }
        return render_template('role/showRole.html', **data)


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
                'userid': session.get('id')
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
        try:
            role = Role.query.filter(Role.id == rid).first()
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
    if_role = request.form.get('if_role')
    if_add_equipment = request.form.get('if_add_equipment')
    if_modify_equipment = request.form.get('if_modify_equipment')
    if_add_child = request.form.get('if_add_child')
    if_modify_child = request.form.get('if_modify_child')
    equipmentInfo = {
        'name': name,
        'create_user': user_id,
        'if_role': if_role,
        'if_add_equipment': if_add_equipment,
        'if_modify_equipment': if_modify_equipment,
        'if_add_child': if_add_child,
        'if_modify_child': if_modify_child
    }

    try:
        role = Role(**equipmentInfo)
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
        展示设备添加页面
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
        data = {
            'base': {
                'pageTitle': '添加设备-云安服务',
                'avatarImgUrl': '/static/img/yunan_logo_1.png',
                'pageNow': '添加设备',
                'username': session.get('username'),
                'userid': session.get('id')
            }
        }
        return render_template('role/addrole.html', **data)