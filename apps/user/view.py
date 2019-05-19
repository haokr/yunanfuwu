from flask import request, session, render_template, redirect, url_for, jsonify
from models import User, Group
from db import db
import time


'''
    Page
'''

def root():
    '''
        获取登陆用户
        未登录返回登陆页面
    :return:
    '''
    if session.get('username'):
        return redirect(url_for('monitor.monitorPage'))
    else:
        return redirect(url_for('user.login'))


def login():
    '''
        获取用户用户名及密码
        验证用户
    :return:
    '''
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username == username, User.password==password).first()
    if user:
        session['id'] = user.id
        session['username'] = username
        return redirect(url_for('monitor.monitorPage'))
    else:
        return redirect(url_for('user.login'))


def logout():
    '''
        用户登出
    :return:
    '''
    session.clear()
    return redirect(url_for('user.login'))


def getlogin():
    '''
        返回登陆页面
    :return:
    '''
    return render_template('login.html')


def registerPage():
    '''
        用户注册
    :return:
    '''
    return render_template('register.html')


def register():
    '''
        获取用户提交信息
        实现用户注册及存储
    :return:
    '''
    username = request.form.get('username')
    password = request.form.get('password')
    registerData = {
        'username': username,
        'password': password
    }
    isExisted = User.query.filter(User.username==username).all()
    if not isExisted:
        try:
            user = User(**registerData)
            db.session.add(user)
            db.session.flush()
            group = Group(admin_id=user.id, name=username)
            db.session.add(group)
            db.session.commit()
            session['id'] = user.id
            session['username'] = username
        except Exception as e:
            print(e)
            return {'msg': 'fail', 'data': 'commit fail'}
    return redirect(url_for('user.root'))


def showAddUser(uid):
    '''
        新增用户展示
    :return:
    '''
    data = {
        'base': {
            'pageTitle': '添加设备-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '添加设备',
            'username': session.get('username'),
            'userid': session.get('id')
        },
        'parent': uid
    }
    return render_template('addUser.html', **data)


def ShowUser(uid):
    '''
        展示账号信息
    :return:
    '''
    user = User.query.filter(User.id == uid).first()
    children = User.query.filter(User.parent_id == uid).all()
    if user.parent == None:
        parentname = '无'
    else:
        parentname = e.parent.username
    data = {
        'base': {
            'pageTitle': '设备信息-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '用户信息',
            'username': session.get('username'),
            'userid': session.get('id')
        },
        'user': {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'parent': parentname,
                'address': user.address,
                'create_time': user.create_time,
                'modify_time': user.modify_time
            },
        'children': [
            {
                'id': c.id,
                'name': c.name,
                'username': c.username,
                'parent': c.parent.username,
                'address': c.address,
                'create_time': c.create_time,
                'modify_time': c.modify_time
            }
            for c in children
        ]
    }
    return render_template('editUser.html', **data)


'''
    API
'''

def modifyUser(uid):
    '''
        获取用户提交要修改的设备信息
        修改设备信息并存储
    :param uid: 用户ID
    :return: 设备信息修改状态
    '''
    key = request.form.get('key')
    value = request.form.get('value')
    if value == '':
        value = None
    try:
        user = User.query.filter(User.id == uid)
        user.update({key: value})
        user.modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.session.commit()
        return jsonify({'msg': 'success', 'data': 'modify equipment success'})
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'data': 'modify equipment error when select equipments'})




def addChild(uid):
    '''
        获取用户提交信息
        实现用户子账号的创建并存储
    :return:
    '''
    username = request.form.get('username')
    password = request.form.get('password')
    name = request.form.get('name')
    address = request.form.get('address')
    describe = request.form.get('describe')
    parent_id = uid
    
    if not (username and password):
        return jsonify({'msg': 'fail', 'data': 'parm error'})

    childData = {
        'username': username,
        'password': password,
        'name': name,
        'address': address,
        'describe': describe,
        'parent_id': parent_id
    }
    isUserExisted = User.query.filter(User.username == childData['username']).all()
    if not isUserExisted:
        try:
            user = User(**childData)
            db.session.add(user)
            db.session.flush()
            group = Group(admin_id=user.id, name=childData['username'])
            db.session.add(group)
            db.session.commit()
            return jsonify({'msg': 'success', 'data': 'add success'})
        except Exception as e:
            print(e)
            return jsonify({'msg': 'fail', 'data': 'create child error when commit database'})
    else:
        user = User.query.filter(User.username == childData['username']).first()
        user_id = user.id
        isGroupExisted = Group.query.filter(Group.admin_id == user_id).all()
        if not isGroupExisted:
            try:
                group = Group(admin_id=user_id, name=childData['username'])
                db.session.add(group)
                db.session.commit()
            except Exception as e:
                return jsonify({'msg': 'fail', 'data': 'create gruop fail when commit database'})
        return jsonify({'msg': 'fail', 'data': 'the username is existed'})
