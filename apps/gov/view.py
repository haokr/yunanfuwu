from flask import request, session, jsonify, render_template, url_for, redirect
from models import Gov, Equipment, Alarm_record
from db import db
from sqlalchemy import extract, and_
from datetime import datetime, timedelta
import time
import requests


def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = Gov.query.filter(Gov.username == username, Gov.password==password).first()
    if user:
        session['id'] = user.id
        session['username'] = username
        session['name'] = user.name
        return redirect(url_for('gov.monitor'))
    else:
        return redirect(url_for('gov.login'))

def logout():
    session.clear()
    return jsonify({'msg': 'success'})

def regist():
    username = request.form.get('username')		
    password = request.form.get('password')
    gaode_center_longitude = request.form.get('gaode_center_longitude')
    gaode_center_latitude = request.form.get('gaode_center_latitude')
    name = request.form.get('name')

    if not(name and gaode_center_latitude and gaode_center_longitude and username and password):
    	return 'error parm'
    try:
        govData = {
    		'username': username,
    		'password': password,
    		'name': name,
    		'gaode_center_latitude': gaode_center_latitude,
    		'gaode_center_longitude': gaode_center_longitude
    	}
        gov = Gov(**govData)
        db.session.add(gov)
        db.session.commit()
        session['id'] = gov.id
        session['username'] = username
        session['name'] = gov.name

    except Exception as e:
    	print(e)
    	return 'db commit error when regist'

    return 'success'




def loginPage():
	return render_template('gov/login.html')


def monitor():
    user_id = session.get('id')
    user_name = session.get('name')
    gov = Gov.query.filter(Gov.id == user_id).first()

    gaode_center_longitude = gov.gaode_center_longitude
    gaode_center_latitude = gov.gaode_center_latitude

    level = gov.level

    equipments = []
    cityData = {}

    if level == 1:
        province = gov.province

        cityData = requests.get('https://restapi.amap.com/v3/config/district?key=1f5f34e6c96735e4be689afb6ec22a82&keywords='+province).json()
        equipments = [
            {
            'id': e.id,
            'name': e.name,
            'class_': e.class_,
            'gaode_longitude': e.gaode_longitude,
            'gaode_latitude': e.gaode_latitude,
            'location': e.location,
            'ip': e.ip,
            'use_department': e.use_department,
            'remarks': e.remarks,
            'manufacturer': e.manufacturer,
            'model': e.model,
            'position_province': e.position_province,
            'position_city': e.position_city,
            'position_district': e.position_district,
            'create_time': e.create_time,
            'status': e.status,
            'SIM_id': e.SIM_id,
            'modify_time': e.modify_time
            }
            for e in Equipment.query.filter(Equipment.position_province == province, Equipment.live == True).all()
        ]
    elif level == 2:
        province = gov.province
        city = gov.city        
        cityData = requests.get('https://restapi.amap.com/v3/config/district?key=1f5f34e6c96735e4be689afb6ec22a82&keywords='+city).json()

        equipments = [
            {
            'id': e.id,
            'name': e.name,
            'class_': e.class_,
            'gaode_longitude': e.gaode_longitude,
            'gaode_latitude': e.gaode_latitude,
            'location': e.location,
            'ip': e.ip,
            'use_department': e.use_department,
            'remarks': e.remarks,
            'manufacturer': e.manufacturer,
            'model': e.model,
            'position_province': e.position_province,
            'position_city': e.position_city,
            'position_district': e.position_district,
            'create_time': e.create_time,
            'status': e.status,
            'SIM_id': e.SIM_id,
            'modify_time': e.modify_time
            }
            for e in Equipment.query.filter(Equipment.position_province == province, Equipment.live == True, Equipment.position_city == city).all()
        ]
    elif level == 3:
        province = gov.province
        city = gov.city
        district = gov.district
        cityData = requests.get('https://restapi.amap.com/v3/config/district?key=1f5f34e6c96735e4be689afb6ec22a82&keywords='+district).json()

        equipments = [
            {
            'id': e.id,
            'name': e.name,
            'class_': e.class_,
            'gaode_longitude': e.gaode_longitude,
            'gaode_latitude': e.gaode_latitude,
            'location': e.location,
            'ip': e.ip,
            'use_department': e.use_department,
            'remarks': e.remarks,
            'manufacturer': e.manufacturer,
            'model': e.model,
            'position_province': e.position_province,
            'position_city': e.position_city,
            'position_district': e.position_district,
            'create_time': e.create_time,
            'status': e.status,
            'SIM_id': e.SIM_id,
            'modify_time': e.modify_time
            }
            for e in Equipment.query.filter(Equipment.position_province == province, Equipment.live == True, Equipment.position_city == city, Equipment.district == district).all()
        ]

    returnData = {
        'base': {
            'gov_id': session.get('id'),
            'gov_name': session.get('name'),
            'gaode_longitude': gaode_center_longitude,
            'gaode_latitude': gaode_center_latitude,
            'pageNow': '设备监控',
            'level': level,
            'city': cityData['districts'][0]
        },
        'equipments': equipments
    }

    return render_template('gov/monitor.html', **returnData)


def datashow():
    user_id = session.get('id')
    user_name = session.get('name')
    gov = Gov.query.filter(Gov.id == user_id).first()

    gaode_center_longitude = gov.gaode_center_longitude
    gaode_center_latitude = gov.gaode_center_latitude

    level = gov.level

    equipments = []
    cityData = {}
    if level == 1:
        province = gov.province
        cityData = requests.get('https://restapi.amap.com/v3/config/district?key=1f5f34e6c96735e4be689afb6ec22a82&keywords='+province).json()
        equipments = Equipment.query.filter(Equipment.position_province == province, Equipment.live == True).all()
    elif level == 2:
        province = gov.province
        city = gov.city
        cityData = requests.get('https://restapi.amap.com/v3/config/district?key=1f5f34e6c96735e4be689afb6ec22a82&keywords='+city).json()
        equipments = Equipment.query.filter(Equipment.position_province == province, Equipment.live == True, Equipment.position_city == city).all()
    elif level == 3:
        province = gov.province
        city = gov.city
        district = gov.district
        cityData = requests.get('https://restapi.amap.com/v3/config/district?key=1f5f34e6c96735e4be689afb6ec22a82&keywords='+district).json()
        equipments = Equipment.query.filter(Equipment.position_province == province, Equipment.live == True, Equipment.position_city == city, Equipment.district == district).all()
    equipmentIds = [e.id for e in equipments if e.live == True]
    equipmentCount = len(equipments)
    # 今日报警信息
    now = datetime.now()
    to_day = now.day
    to_month = now.month
    to_year = now.year

    reports = Alarm_record.query.filter(Alarm_record.equipment_id.in_(equipmentIds), and_(
        extract('year', Alarm_record.alarm_time) == to_year,
        extract('month', Alarm_record.alarm_time) == to_month,
        extract('day', Alarm_record.alarm_time) == to_day
    )).all()

    todayAlarmCount = 0
    todayFaultCount = 0
    nowAlarmCount = 0
    nowFaultCount = 0

    for re in reports:
        if re.class_ == '报警':
            todayAlarmCount += 1
            if re.operator_id == None:
                nowAlarmCount += 1
        else:
            todayFaultCount += 1
            if re.operator_id == None:
                nowFaultCount += 1
    # 过去两周报警信息统计
    beginDay = datetime(to_year, to_month, to_day - 14)
    twoWeeksReportCounts = []
    for i in range(14):
        begin = beginDay + timedelta(days=i)
        end = begin + timedelta(days=1)

        dailyAlarmCount = Alarm_record.query.filter(Alarm_record.alarm_time.between(begin, end)).count()

        twoWeeksReportCounts.append(dailyAlarmCount)
    twoWeeksDays = [int(time.mktime((beginDay + timedelta(days=i)).timetuple())) * 1000 for i in range(14)]

    returnData = {
        'base': {
            'gov_id': session.get('id'),
            'gov_name': session.get('name'),
            'gaode_longitude': gaode_center_longitude,
            'gaode_latitude': gaode_center_latitude,
            'pageNow': '数据展示',
            'level': level,
            'city': cityData['districts'][0]
        },
        'data': {
            'equipmentCount': equipmentCount,
            'nowAlarmCount': nowAlarmCount,
            'nowFaultCount': nowFaultCount,
            'todayAlarmCount': todayAlarmCount,
            'todayFaultCount': todayFaultCount,
            'twoWeeksDays': twoWeeksDays,
            'twoWeeksReportCounts': twoWeeksReportCounts

        }
    }

    return render_template('gov/showdata.html', **returnData)

def alarm_record():
    user_id = session.get('id')
    user_name = session.get('name')
    gov = Gov.query.filter(Gov.id == user_id).first()

    gaode_center_longitude = gov.gaode_center_longitude
    gaode_center_latitude = gov.gaode_center_latitude

    level = gov.level

    equipments = []
    cityData = {}

    if level == 1:
        province = gov.province

        cityData = requests.get('https://restapi.amap.com/v3/config/district?key=1f5f34e6c96735e4be689afb6ec22a82&keywords='+province).json()
        equipments = [
            {
            'id': e.id,
            'name': e.name,
            'class_': e.class_,
            'gaode_longitude': e.gaode_longitude,
            'gaode_latitude': e.gaode_latitude,
            'location': e.location,
            'ip': e.ip,
            'use_department': e.use_department,
            'remarks': e.remarks,
            'manufacturer': e.manufacturer,
            'model': e.model,
            'position_province': e.position_province,
            'position_city': e.position_city,
            'position_district': e.position_district,
            'create_time': e.create_time,
            'status': e.status,
            'SIM_id': e.SIM_id,
            'modify_time': e.modify_time
            }
            for e in Equipment.query.filter(Equipment.position_province == province, Equipment.live == True).all()
        ]
    elif level == 2:
        province = gov.province
        city = gov.city        
        cityData = requests.get('https://restapi.amap.com/v3/config/district?key=1f5f34e6c96735e4be689afb6ec22a82&keywords='+city).json()

        equipments = [
            {
            'id': e.id,
            'name': e.name,
            'class_': e.class_,
            'gaode_longitude': e.gaode_longitude,
            'gaode_latitude': e.gaode_latitude,
            'location': e.location,
            'ip': e.ip,
            'use_department': e.use_department,
            'remarks': e.remarks,
            'manufacturer': e.manufacturer,
            'model': e.model,
            'position_province': e.position_province,
            'position_city': e.position_city,
            'position_district': e.position_district,
            'create_time': e.create_time,
            'status': e.status,
            'SIM_id': e.SIM_id,
            'modify_time': e.modify_time
            }
            for e in Equipment.query.filter(Equipment.position_province == province, Equipment.live == True, Equipment.position_city == city).all()
        ]
    elif level == 3:
        province = gov.province
        city = gov.city
        district = gov.district
        cityData = requests.get('https://restapi.amap.com/v3/config/district?key=1f5f34e6c96735e4be689afb6ec22a82&keywords='+district).json()

        equipments = [
            {
            'id': e.id,
            'name': e.name,
            'class_': e.class_,
            'gaode_longitude': e.gaode_longitude,
            'gaode_latitude': e.gaode_latitude,
            'location': e.location,
            'ip': e.ip,
            'use_department': e.use_department,
            'remarks': e.remarks,
            'manufacturer': e.manufacturer,
            'model': e.model,
            'position_province': e.position_province,
            'position_city': e.position_city,
            'position_district': e.position_district,
            'create_time': e.create_time,
            'status': e.status,
            'SIM_id': e.SIM_id,
            'modify_time': e.modify_time
            }
            for e in Equipment.query.filter(Equipment.position_province == province, Equipment.live == True, Equipment.position_city == city, Equipment.district == district).all()
        ]
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

    returnData = {
        'base': {
            'gov_id': session.get('id'),
            'gov_name': session.get('name'),
            'gaode_longitude': gaode_center_longitude,
            'gaode_latitude': gaode_center_latitude,
            'level': level,
            'city': cityData['districts'][0]
        },
        'alarm_records': alarm_records
    }

    return render_template('gov/alarm_record.html', **returnData)