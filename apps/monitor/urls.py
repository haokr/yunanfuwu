from flask import Blueprint, request, session
from flask_socketio import send, emit
from socketIO import socketio
from apps.monitor import view

monitor = Blueprint('monitor', __name__) 


'''
    Page
'''

# 展示设备传回信息的路由
@monitor.route('/')
def monitorPage():
    return view.monitorPage()

@monitor.route('/electrical')
def electricalMonitorPage():
	return view.electricalMonitorPage()

@monitor.route("/report")
def reportPage():
	return view.reportPage()
'''
    report
'''

# 修改设备状态的路由
@monitor.route('/report/<eid>', methods=['POST'])
def report(eid):
    return view.report(eid)

@monitor.route('/uireport/<eid>', methods=['POST'])
def UIReport(eid):
    return view.UIReport(eid)

'''
    WebSocketIO
'''

# 获取用户设备信息的路由
@socketio.on('connect')
def connect():
    return view.connect()


# 将设备新增进组的路由
@monitor.route('/join/<eid>', methods=['POST'])
def join(eid):
    return view.joinRoom(eid)


# 微信上设备展示
@monitor.route('/wxshow', methods=['GET'])
def wx_showEquipments():
    return view.wx_showEquipments()
