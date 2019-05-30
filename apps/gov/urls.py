from flask import Blueprint, request
import apps.gov.view as view

gov = Blueprint('gov', __name__)


@gov.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		return view.login()
	else:
		return view.loginPage()

@gov.route('/logout', methods=['POST'])
def logout():
	return view.logout()

@gov.route('/regist', methods=['POST'])
def regist():
	return view.regist()

@gov.route('/monitor')
def monitor():
	return view.monitor()

@gov.route('/alarmrecord')
def alarm_record():
	return view.alarm_record()