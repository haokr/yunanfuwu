from flask import Blueprint, request
import apps.equipment.view as view

equipment = Blueprint('equipment', __name__)

'''
    Page
'''

# 展示新增设备
@equipment.route('/show/add')
def showAddEquipment():
    return view.showAddEquipment()


# 展示设备信息
@equipment.route('/show/<eid>')
def showEditEquipment(eid):
    return view.showEditEquipment(eid)


# 设备展示
@equipment.route('/show')
def showEquipments():
    return view.showEquipments()


'''
    API
'''

# 修改设备信息
@equipment.route('/<eid>', methods=['POST'])
def modify(eid):
    return view.modifyEquipment(eid)


# 添加设备
@equipment.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'GET':
        return view.getEquipments()
    else:
        return view.addEquipment()