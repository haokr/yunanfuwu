# -*- coding: utf-8 -*-

from db import db
import shortuuid
from datetime import datetime

# 父子账号关系中间表
parent_child_user_relationship = db.Table('parent_child_user_relationship',
        db.Column('parent_id', db.String(30), db.ForeignKey('user.id'), primary_key=True),
        db.Column('child_id', db.String(30), db.ForeignKey('user.id'), primary_key=True)
    )

# 用户
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(30), primary_key=True, nullable=False, default='ya_'+shortuuid.uuid())
    name = db.Column(db.String(50), nullable=False, default='YA_User')
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(40), nullable=False)

    # 将 父子账号 通过中间表关联起来
    parent = db.relationship('User', secondary=parent_child_user_relationship, backref=db.backref('child'))
    childs = db.relationship('User', secondary=parent_child_user_relationship, backref=db.backref('parent'))

    group_id = db.Column(db.String(30), db.ForeignKey(group.id))
    group = db.relationship('Group', backref='user')

    address = db.Column(db.String(50))
    describe = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, update=datetime.now)

# 用户操作记录
class user_record(db.Model):
    __tablename__ = 'user_record'
    id = db.Column(db.String(30), primary_key=True, nullable=False, default='ur_'+shortuuid.uuid())
    user_id = db.Column(db.String(30), db.ForeignKey=(user.id))
    user = db.relationship('User', backref='record')
    ip = db.Column(db.Integer, default=0)
    operation = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, update=datetime.now)


