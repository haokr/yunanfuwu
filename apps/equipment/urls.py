from flask import Blueprint, request
import apps.equipment.view as view

equipment = Blueprint('equipment', __name__)

@equipment.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return view.getEquipments()
    else:
        return view.addEquipment()

@equipment.route('/show/<eid>')
def showEditEquipment(eid):
    return view.showEditEquipment(eid)

@equipment.route('/show')
def showEquipments():
    return view.showEquipments()

