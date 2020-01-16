from flask import Blueprint, request, session
from apps.live import view


live = Blueprint('live', __name__)


# 获取直播设备列表
@live.route('/devices', methods=['GET'])
def devices():
    return view.devices()


# 获取直播页面
@live.route('/living', methods=['GET'])
def living():
    session['liveToken'] = "2b25b1f4cfd8411e98539757e10d892c"
    return view.living()

