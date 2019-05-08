from flask import request, session, jsonify, render_template
from models import User, Group, Equipment
from db import db

def getEquipments():
    return jsonify({'msg': 'ok', 'data': 'This root of equipment'})

def addEquipment():
    name = request.form.get('name')
    user_id = session.get('id')
    if not user_id:
        return jsonify({'msg': 'fail', 'data': 'please to login'})
    user = User.query.filter(User.id == user_id).first()
    try:
        equipment = Equipment(name=name)
        equipment.group.append(user.group)
        while user.parent_id:
            user = user.parent
            equipment.group.append(user.group)
        db.session.add(equipment)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'msg': 'fail', 'data': 'add equipment error when commit database'})
    return jsonify({'msg': 'success', 'data': 'add success'})

def showEquipments():
    data = {
        'base':{
            'pageTitle': '设备信息-云安服务',
            'avatarImgUrl': '/static/img/yunan_logo_1.png'
            # 'tipCount': None,
            # 'tips': []
        },
        'equipments': [
            {
                'name': 'wanghao1',
                'status': 'off',
                'use_department': 'dashujv',
                'location': 'mingxiang',
                'remark': '',
                'manufacturer': 'ni',
                'model': 'wu',
                'create_time': '2019-2-2',
                'id': 'e_21312easdsa'
            },
            {
                'name': 'wanghao1',
                'status': 'off',
                'use_department': 'dashujv',
                'location': 'mingxiang',
                'remark': '',
                'manufacturer': 'ni',
                'model': 'wu',
                'create_time': '2019-2-2',
                'id': 'e_21312easdsa'
            },
            {
                'name': 'wanghao1',
                'status': 'off',
                'use_department': 'dashujv',
                'location': 'mingxiang',
                'remark': '',
                'manufacturer': 'ni',
                'model': 'wu',
                'create_time': '2019-2-2',
                'id': 'e_21312easdsa'
            },
            {
                'name': 'wanghao1',
                'status': 'off',
                'use_department': 'dashujv',
                'location': 'mingxiang',
                'remark': '',
                'manufacturer': 'ni',
                'model': 'wu',
                'create_time': '2019-2-2',
                'id': 'e_21312easdsa'
            }
        ]
    }
    return render_template('equipments.html', **data)