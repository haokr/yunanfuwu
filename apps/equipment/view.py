from flask import request, session, jsonify
from models import User, Group, Equipment
from db import db

def getEquipments():
    return jsonify({'msg': 'ok', 'data': 'This root of equipment'})

def addEquipment():
    name = request.form.get('name')
    user_id = session.get('id')
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
