from flask import request, session, render_template, redirect, url_for, jsonify
from models import User
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
    if username == 'wanghao' and password  == 'wanghao':
        user = User.query.filter(User.username == username).first()
        session['id'] = user.id
        session['username'] = username
        return redirect(url_for('user.root'))
    else:
        return redirect(url_for('user.login'))

def getlogin():
    if session.get('username'):
        return redirect(url_for('user.root'))
    else:
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
    isExisted = User.query.filter(User.username==username)
    if not isExisted:
        user = User(**registerData)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
    return redirect(url_for('user.root'))

def showChilds():
    id = session.get('id')
    childs = User.query.filter(User.parent_id == id).all()
    print(childs)
    return 'OK'
def addChild():
    childData = {
        'username': 'wanghaosChild1',
        'password': 'wanghaosChild1',
        'name': '王浩的第一个子节点',
        'address': '山西太原',
        'describe': '太原理工大学明向校区大数据学院802',
        'parent_id': session.get('id')
    }
    user = User(**childData)
    db.session.add(user)
    db.session.commit()
    return jsonify(childData)
