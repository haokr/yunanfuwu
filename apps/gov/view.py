from flask import request, session, jsonify, render_template, url_for, redirect
from models import Gov, Equipment
from db import db

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
                'gaode_latitude': e.gaode_latitude,
                'gaode_longitude': e.gaode_longitude,
                'location': e.location,
                'ip': e.ip,
                'use_department': e.use_department,
                'remarks': e.remarks,
                'manufacturer': e.manufacturer,
                'model': e.model,
                'position_province': e.position_province,
                'position_city': e.position_city,
                'position_district': e.position_district,
                'admin_id': e.admin_id,
                'contact': e.admin.contact,
                'contact_tel': e.admin.contact_tel,
                'status': e.status,
                'create_time': e.create_time
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
                'gaode_latitude': e.gaode_latitude,
                'gaode_longitude': e.gaode_longitude,
                'location': e.location,
                'ip': e.ip,
                'use_department': e.use_department,
                'remarks': e.remarks,
                'manufacturer': e.manufacturer,
                'model': e.model,
                'position_province': e.position_province,
                'position_city': e.position_city,
                'position_district': e.position_district,
                'admin_id': e.admin_id,
                'contact': e.admin.contact,
                'contact_tel': e.admin.contact_tel,
                'status': e.status,
                'create_time': e.create_time
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
                'gaode_latitude': e.gaode_latitude,
                'gaode_longitude': e.gaode_longitude,
                'location': e.location,
                'ip': e.ip,
                'use_department': e.use_department,
                'remarks': e.remarks,
                'manufacturer': e.manufacturer,
                'model': e.model,
                'position_province': e.position_province,
                'position_city': e.position_city,
                'position_district': e.position_district,
                'admin_id': e.admin_id,
                'contact': e.admin.contact,
                'contact_tel': e.admin.contact_tel,
                'status': e.status,
                'create_time': e.create_time
            }
            for e in Equipment.query.filter(Equipment.position_province == province, Equipment.live == True, Equipment.position_city == city, Equipment.district == district).all()
        ]

    returnData = {
        'base': {
            'gov_id': session.get('id'),
            'gov_name': session.get('name'),
            'gaode_longitude': gaode_center_longitude,
            'gaode_latitude': gaode_center_latitude,
            'level': level,
            'city': cityData['districts'][0]
        },
        'equipments': equipments
    }


    return render_template('gov/monitor.html', **returnData)
