from flask import session, render_template, jsonify
from models import User, Equipment, Alarm_record
from sqlalchemy import extract, and_
from datetime import datetime, timedelta


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
    to_day = now.date
    to_month = now.month
    to_year = now.year
    reports = Alarm_record.query.filter(Alarm_record.equipment.admin_id in childrenIds, and_(
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
    twoWeeks = timedelta(days=14)
    endDay = datatime(to_year, to_month, to_day-1)
    beginDay = endDay - twoWeeks
    twoWeeksReports = Alarm_record.query.filter(Alarm_record.create_time.between(beginDay, endDay)).group_by(Alarm_record.create_time.day).all()

    twoWeeksReportCounts = [r.count() for r in twoWeeksReports]

    return jsonify({'msg': 'success', 'data': {
        'equipmentCount': equipmentCount,
        'departmentCount': childCount,
        'nowAlarmCount': nowAlarmCount,
        'nowFaultCount': nowFaultCount,
        'todayAlarmCount': todayAlarmCount,
        'todayFaultCount': todayFaultCount,
        'twoWeeksReportCounts': twoWeeksReportCounts,
        'twoWeeksDays': [ beginDay+timedelta(days=i) for i in range(14)]
    }})

