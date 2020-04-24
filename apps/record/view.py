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