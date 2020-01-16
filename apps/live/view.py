from flask import request, session, jsonify, render_template, url_for, redirect
from utils import *


def devices():
    data = {
        'base':{
            'pageTitle': '监控设备-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '监控设备',
            'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id')
        },
        'devices': [
            {'name': 'test1', 'href': "#"},
            {'name': 'test2', 'href': '#'}
            ]
    }
    return render_template('live/devices.html', **data)


def living(device_id):
    data = {
        'base':{
            'pageTitle': '实时监控-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png',
            'pageNow': '实时监控',
            'username': session.get('username'),
            'name': session.get('name'),
            'userid': session.get('id')
        },
    }
    return render_template('live/living.html', **data)


def closeLive(liveToken):
    return close_live(liveToken)
    
