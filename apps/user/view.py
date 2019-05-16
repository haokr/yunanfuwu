from flask import request, session, render_template, redirect, url_for, jsonify
from models import User, Group
from db import db
import time


def root():
    '''
        获取登陆用户
        未登录返回登陆页面
    :return:
    '''
    if session.get('username'):
        templateData = {
            'username': session.get('username')
        }
        return render_template('index.html', **templateData)
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


def showChilds():
    '''
        获取当前用户ID
        展示用户的子账号
    :return:
    '''
    id = session.get('id')
    childs = User.query.filter(User.parent_id == id).all()
    print(childs)
    return 'OK'


def addChild():
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
    parent_id = session.get('id')
    
    if not ( username and password and parent_id ) :
        return jsonify({'msg': 'fail', 'data': 'parm error'})

    childData = {
        'username': username,
        'password': password,
        'name': name,
        'address': address,
        'describe': describe,
        'parent_id': session.get('id')
    }
    isUserExisted = User.query.filter(User.username==childData['username']).all()
    if not isUserExisted:
        try:
            user = User(**childData)
            db.session.add(user)
            db.session.flush()
            group = Group(admin_id=user.id, name=childData['username'])
            db.session.add(group)
            db.session.commit()
            
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
    return jsonify(childData)


def ShowUser(uid):
    '''
        展示账号信息
    :return:
    '''
    e = User.query.filter(User.id == uid).first()
    children = User.query.filter(User.parent_id == uid).all()
    if e.parent == None:
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
                'id': e.id,
                'name': e.name,
                'username': e.username,
                'parent': parentname,
                'address': e.address,
                'create_time': e.create_time,
                'modify_time': e.modify_time
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


def modifyUser(uid):
    '''
        获取用户提交要修改的设备信息
        修改设备信息并存储
    :param eid: 用户ID
    :return: 设备信息修改状态
    '''
    key = request.form.get('key')
    value = request.form.get('value')
    if value == '':
        value = None
    try:
        print(key, value)
        user = User.query.filter(User.id == uid)
        user.update({key: value})
        user.modify_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        db.session.commit()
        return jsonify({'msg': 'success', 'data': 'modify equipment success'})
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'data': 'modify equipment error when select equipments'})
