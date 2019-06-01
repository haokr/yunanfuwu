from flask import session, render_template, jsonify
from models import User, Equipment, Alarm_record
from sqlalchemy import extract, and_
from datetime import datetime, timedelta
import time
from db import db


'''
    Page
'''

def dataPage():

    user_id = session.get('id')
    user = User.query.filter(User.id == user_id).first()
    # 设备信息
    equipments = user.group.equipments
    equipmentIds = [e.id for e in equipments if e.live == True]
    equipmentCount = len(equipments)
    # 单位信息
    children = user.children
    childCount = children.count()
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
    beginDay = datetime(to_year, to_month, to_day-14)     
    twoWeeksReportCounts = []
    for i in range(14):
        begin = beginDay + timedelta(days=i)
        end = begin + timedelta(days=1)

        dailyAlarmCount = Alarm_record.query.filter(Alarm_record.alarm_time.between(begin, end)).count()

        twoWeeksReportCounts.append(dailyAlarmCount)



    # return jsonify({'msg': 'success', 'data': {
    #     'equipmentCount': equipmentCount,
    #     'departmentCount': childCount,
    #     'nowAlarmCount': nowAlarmCount,
    #     'nowFaultCount': nowFaultCount,
    #     'todayAlarmCount': todayAlarmCount,
    #     'todayFaultCount': todayFaultCount,
    #     'twoWeeksReportCounts': twoWeeksReportCounts,
    #     'twoWeeksDays': [ (beginDay+timedelta(days=i)).strftime("%Y-%m-%d") for i in range(14)]
    # }})

    twoWeeksDays = [ int(time.mktime((beginDay+timedelta(days=i)).timetuple()))*1000 for i in range(14)]

    # lineChartData = list(zip(twoWeeksDays, twoWeeksReportCounts))
    # print(lineChartData)

    data = {
        'base': {
            'pageTitle': '监控-云安服务',
            'pageNow': '设备监控',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id')
        },
        'data': {
            'equipmentCount': equipmentCount,
            'departmentCount': childCount,
            'nowAlarmCount': nowAlarmCount,
            'nowFaultCount': nowFaultCount,
            'todayAlarmCount': todayAlarmCount,
            'todayFaultCount': todayFaultCount,
            'twoWeeksDays': twoWeeksDays,
            'twoWeeksReportCounts': twoWeeksReportCounts
            
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
    equipments = user.group.equipments
    equipmentIds = [e.id for e in equipments]
    equipmentCount = len(equipments)
    # 单位信息
    children = user.children
    childCount = children.count()
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
    beginDay = datetime(to_year, to_month, to_day-14)     
    twoWeeksReportCounts = []
    for i in range(14):
        begin = beginDay + timedelta(days=i)
        end = begin + timedelta(days=1)

        dailyAlarmCount = Alarm_record.query.filter(Alarm_record.alarm_time.between(begin, end)).count()

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

