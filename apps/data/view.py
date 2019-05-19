from flask import session, render_template


def root():
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