from flask import session, render_template, jsonify
from models import User, Equipment, Alarm_record
from sqlalchemy import extract, and_
from datetime import datetime, timedelta
from db import db


'''
    Page
'''

def dataPage():
    data = {
        'base': {
            'pageTitle': '监控-云安服务',
            'pageNow': '设备监控',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'username': session.get('username'),
            'userid': session.get('id')
        }
    }
    return render_template('data/data.html', **data)


'''
    API
'''

def baseData():
    user_id = session.get('id')
    user = User.query.filter(User.id == user_id).first()
    # 设备信息
    equipments = user.equipments
    equipmentCount = equipments.count()
    # 单位信息
    children = user.children
    childrenIds = [c.id for c in children]
    childCount = children.count()
    # 今日报警信息
    now = datetime.now()
    to_day = now.day
    to_month = now.month
    to_year = now.year

    reports = Alarm_record.query.join(Equipment, Alarm_record.equipment_id == Equipment.id).filter(Equipment.admin_id.in_(childrenIds), and_(
        extract('year', Alarm_record.create_time) == to_year,
        extract('month', Alarm_record.create_time) == to_month,
        extract('day', Alarm_record.create_time) == to_day
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
    beginDay = datetime(to_year, to_month, to_day-14)     
    twoWeeksReportCounts = []
    for i in range(14):
        endDay = beginDay + timedelta(days=i+1)

        dailyAlarmCount = Alarm_record.query.filter(Alarm_record.create_time.between(beginDay, endDay)).count()

        twoWeeksReportCounts.append(dailyAlarmCount)

    return jsonify({'msg': 'success', 'data': {
        'equipmentCount': equipmentCount,
        'departmentCount': childCount,
        'nowAlarmCount': nowAlarmCount,
        'nowFaultCount': nowFaultCount,
        'todayAlarmCount': todayAlarmCount,
        'todayFaultCount': todayFaultCount,
        'twoWeeksReportCounts': twoWeeksReportCounts,
        'twoWeeksDays': [ (beginDay+timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14)]
    }})

