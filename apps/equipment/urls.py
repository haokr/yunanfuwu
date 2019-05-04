from flask import Blueprint, request
import apps.equipment.view as view

equipment = Blueprint('equipment', __name__)

@equipment.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GHT':
        return view.getEquipments()
    elif request.method == 'POST':
        return view.addEquipment()

