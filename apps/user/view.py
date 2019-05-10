from flask import request, session, render_template, redirect, url_for, jsonify
from models import User, Group
from db import db

def root():
    if session.get('username'):
        templateData = {
            'username': session.get('username')
        }
        return render_template('index.html', **templateData)
    else:
        return redirect(url_for('user.login'))

def login():
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
    session.clear()
    return redirect(url_for('user.login'))

def getlogin():
    return render_template('login.html')

def registerPage():
    return render_template('register.html')

def register():
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
    id = session.get('id')
    childs = User.query.filter(User.parent_id == id).all()
    print(childs)
    return 'OK'
def addChild():
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
