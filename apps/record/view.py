from flask import session, render_template
from db import db
from datetime import datetime
from models import Alarm_record, User


def root():
	user_id = session.get('id')
	user = User.query.filter(User.id == user_id).first()
	equipments = user.group.equipments

	children = User.query.filter(User.parent_id == user_id, User.live == True).all()

	alarm_records = []

	for e in equipments:
		for r in e.alarm_records:
			alarm_records.append({
				'e_id': e.id,
				'e_name': e.name,
				'e_location': e.location,
				'admin_id': e.admin.id,
				'admin_name': e.admin.name,
				'contact': e.admin.contact,
				'contact_tel': e.admin.contact_tel,
				'alarm_id': r.id,
				'class_': r.class_,
				'alarm_time': datetime.strftime(r.alarm_time, "%Y-%m-%d %H:%M:%S")
			})
			alarm_records.sort(key=lambda a: a['alarm_time'], reverse=True)
	data = {
		'base': {
			'pageTitle': '报警记录-云安服务',
            'pageNow': '报警记录',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id'),
			'children' : [
                {
                    'id': c.id,
                    'name': c.name
                }
                for c in children
            ],
		},
		'alarm_records': alarm_records
	}
	return render_template('record/alarm_record.html', **data)


def data_record():
    user_id = session.get('id')

    user = User.query.filter(User.id == user_id).first()
    equipments = user.group.equipments

    children = User.query.filter(User.parent_id == user_id, User.live == True).all()

    data_records = []

    for e in equipments:
        for r in e.data_records:
            data_records.append({
                'e_id': e.id,
                'e_name': e.name,
                'admin_id': e.admin.id,
                'admin_name': e.admin.name,
                'contact': e.admin.contact,
                'contact_tel': e.admin.contact_tel,
                'use_department': e.use_department,
                'e_class': e.class_,
                'record_id': r.id,
                'data': r.data,
                'class_': r.class_,
                'record_time': datetime.strftime(r.record_time, "%Y-%m-%d %H:%M:%S")
            })
        data_records.sort(key=lambda a: a['record_time'], reverse=True)
    data = {
        'base': {
            'pageTitle': '上报数据记录-云安服务',
            'pageNow': '上报数据记录',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
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
        'data_records': data_records
    }
    return render_template('record/data_record.html', **data)


def ui_record():
    user_id = session.get('id')

    user = User.query.filter(User.id == user_id).first()
    equipments = user.group.equipments

    children = User.query.filter(User.parent_id == user_id, User.live == True).all()

    ui_records = []

    for e in equipments:
        for r in e.ui_report_logs:
            ui_records.append({
                'e_id': e.id,
                'e_name': e.name,
                'admin_id': e.admin.id,
                'admin_name': e.admin.name,
                'contact': e.admin.contact,
                'contact_tel': e.admin.contact_tel,
                'use_department': e.use_department,
                'e_class': e.class_,
                'record_id': r.id,
                'data': {
                    'HighPositiveActiveTotalElectricEnergy': r.HighPositiveActiveTotalElectricEnergy,
                    'HighPositiveTotalReactivePower': r.HighPositiveTotalReactivePower,

                    'AphaseVoltage': r.AphaseVoltage,
                    'BphaseVoltage': r.BphaseVoltage,
                    'CphaseVoltage': r.CphaseVoltage,

                    'AphaseCurrent': r.AphaseCurrent,
                    'BphaseCurrent': r.BphaseCurrent,
                    'CphaseCurrent': r.CphaseCurrent,

                    'TotalActivePowerHigh': r.TotalActivePowerHigh,
                    'AphaseActivePower': r.AphaseActivePower,
                    'BphaseActivePower': r.BphaseActivePower,
                    'CphaseActivePpwer': r.CphaseActivePpwer,
                },
                'class_': r.class_,
                'report_time': datetime.strftime(r.report_time, "%Y-%m-%d %H:%M:%S")
            })
        ui_records.sort(key=lambda a: a['report_time'], reverse=True)
    data = {
        'base': {
            'pageTitle': '电气数据记录-云安服务',
            'pageNow': '电气数据记录',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
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
        'ui_records': ui_records
    }
    return render_template('record/ui_record.html', **data)