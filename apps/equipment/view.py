from flask import request, session
from models import User, Group, Equipment
from db import db

def getEquipments():
    return 'This root of equipment'

def addEquipment():
    name = request.form.get('name')
    try:
        equipment = Equipment(name=name)
        db.session.add(equipment)
        db.session.commit()
    except Exception as e:
        print(e)
        return {'msg': 'fail', 'data': 'add equipment error when commit database'}
    return {'msg': 'success', 'data': 'add success'}
