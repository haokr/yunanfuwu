# -*- coding: utf-8 -*-

from db import db
import shortuuid
from datetime import datetime


# 设备分组关系中间表
equipment_group_relationship = db.Table('equipment_group_relationship',
        db.Column('group_id', db.String(30), db.ForeignKey('group.id'), primary_key=True),
        db.Column('equipment_id', db.String(30), db.ForeignKey('equipment.id'), primary_key=True),
        db.Column('create_time', db.DateTime, default=datetime.now)
    )


# 角色
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.String(30), primary_key=True, nullable=False, default=lambda: 'ro_' + shortuuid.uuid())
    name = db.Column(db.String(30), nullable=False, default='DEFAULT')
    user = db.relationship('User', backref=db.backref('role'))
    create_user = db.Column(db.String(30), nullable=False)

    if_role = db.Column(db.BOOLEAN, nullable=False, default=True)

    if_add_equipment = db.Column(db.BOOLEAN, nullable=False, default=False)
    if_modify_equipment = db.Column(db.BOOLEAN, nullable=False, default=False)

    if_add_child = db.Column(db.BOOLEAN, nullable=False, default=False)
    if_modify_child = db.Column(db.BOOLEAN, nullable=False, default=False)

    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# 用户
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(30), primary_key=True, nullable=False, default=lambda: 'u_' + shortuuid.uuid())
    name = db.Column(db.String(50), nullable=False, index=True, default='YA_User')
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    contact = db.Column(db.String(15))
    contact_tel = db.Column(db.String(15))

    parent_id = db.Column(db.String(30), db.ForeignKey('user.id'))
    parent = db.relationship('User',remote_side=[id], backref=db.backref('children', lazy='dynamic'))

    role_id = db.Column(db.String(30), db.ForeignKey('role.id'))

    group = db.relationship('Group', uselist=False)

    if_Administrative = db.Column(db.BOOLEAN, nullable=False, default=False)

    address = db.Column(db.String(50))
    describe = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# 用户操作记录
class User_record(db.Model):
    __tablename__ = 'user_record'
    id = db.Column(db.String(30), primary_key=True, nullable=False, default=lambda : 'ur_' + shortuuid.uuid())
    user_id = db.Column(db.String(30), db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('record', lazy='dynamic'))
    ip = db.Column(db.String(24))
    operation = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# 分组管理
class Group(db.Model):
    __tablename__ = 'group'
    id = db.Column(db.String(30), primary_key=True, nullable=False, default=lambda : 'g_' + shortuuid.uuid())
    name = db.Column(db.String(30), nullable=False, default='GROUPNAME')

    # 将 设备分组 通过中间表关联起来
    equipments = db.relationship('Equipment', secondary=equipment_group_relationship, backref=db.backref('group', lazy='dynamic'))

    admin_id = db.Column(db.String(30), db.ForeignKey('user.id'))
    admin = db.relationship('User', uselist=False)

    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# 设备
class Equipment(db.Model):
    __equipment__ = 'equipment'
    id = db.Column(db.String(30), primary_key=True, nullable=False, default=lambda : 'e_' + shortuuid.uuid())
    name = db.Column(db.String(30), nullable=False)
    class_ = db.Column(db.String(20), nullable=False)
    gaode_longitude = db.Column(db.Float())
    gaode_latitude = db.Column(db.Float())
    location = db.Column(db.String(30))
    ip = db.Column(db.String(24), unique=True)
    use_department = db.Column(db.String(30))
    remarks = db.Column(db.String(50))
    manufacturer = db.Column(db.String(30))
    model = db.Column(db.String(15))

    admin_id = db.Column(db.String(30), db.ForeignKey('user.id'))
    admin = db.relationship('User', backref=db.backref('equipments', lazy='dynamic'))

    status = db.Column(db.String(15), default='off')
    SIM_id = db.Column(db.String(20), default='0')
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# 报警记录
class Alarm_record(db.Model):
    __tablename__ = 'alarm_record'
    id = db.Column(db.String(30), primary_key=True, nullable=False, default=lambda : 'ar_' + shortuuid.uuid())

    equipment_id = db.Column(db.String(30), db.ForeignKey('equipment.id'))
    equipment = db.relationship('Equipment', backref=db.backref('alarm_records', lazy='dynamic'))

    class_ = db.Column(db.String(10), nullable=False)

    operator_id = db.Column(db.String(30), db.ForeignKey('user.id'))
    operator = db.relationship('User', backref=db.backref('dealed_alarms', lazy='dynamic'))

    deal_describe = db.Column(db.String(50))

    alarm_time = db.Column(db.DateTime, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


# 设备日志
class Equipment_report_log(db.Model):
    __tablename__ = 'equipment_report_log'
    id = db.Column(db.String(30), primary_key=True, nullable=False, default=lambda: 'erl_' + shortuuid.uuid())
    
    equipment_id = db.Column(db.String(30), db.ForeignKey('equipment.id'))
    equipment = db.relationship('Equipment', backref=db.backref('report_logs', lazy='dynamic'))

    class_ = db.Column(db.String(10), nullable=False)

    report_time = db.Column(db.DateTime, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    modify_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)



