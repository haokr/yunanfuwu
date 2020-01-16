# from flask import g
import hashlib
import json
import random
import string
import time
from copy import deepcopy
import requests

# 基本的api
api = "https://openapi.lechange.cn/openapi/"
# 获取当前时间，单位为秒
time = round(time.time())
# 随机生成32位字符串，要求5分钟内不能重复
nonce = "".join(random.choices(string.digits + "abcdef", k=32))
app_secret = "43be721f9ce84bd2bc09164ddcbae7"
# 生成md5值
sign = hashlib.md5(
    f"time:{time},nonce:{nonce},appSecret:{app_secret}".encode()).hexdigest()

data = {
    "system": {
        "ver": "1.0",
        "sign": sign,
        "appId": "lc3cb586d5ab8649ea",
        "time": time,
        "nonce": nonce
    },
    "params": {},
    "id": "".join(random.choices(string.digits + "abcdef", k=6))
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/79.0.3945.117 Safari/537.36',
}
# accessToken = g['accessToken']
accessToken = "At_93580388aae0411ea536d5c0aa1eebe3"

def get_admin_access_token():
    """
    获取管理员模式token
    :return: accessToken
    """
    res = requests.post(api + "accessToken",
                        data=json.dumps(data),
                        headers=headers)
    print(res.text)
    response = res.json()
    print(response)
    if response['result']['code'] == "0":
        return response['result']['data']['accessToken']
    else:
        return False


def get_user_access_token():
    """
    获取用户模式token
    :return: accessToken
    """

    pass


def get_device_base_list():
    """
    获取乐橙客户端添加或者分享的设备通道基本信息
    :return: 设备deviceId列表
    """
    data['params'] = {
        'token': accessToken,
        'bindId': -1,
        'limit': 10,
        'type': 'bindAndShare',
        'needApInfo': False
    }
    res = requests.post(api + "deviceBaseList",
                        data=json.dumps(data),
                        headers=headers)
    response = res.json()
    if response['result']['code'] == "0":
        return response['result']['data']['accessToken']
    else:
        return False


def get_set_device_snap_enhanced(device_id):
    """
    设备抓图。
    :return: 图片地址
    """
    data['params'] = {
        'token': accessToken,
        'deviceId': device_id,
        'channelId': 0,
    }
    res = requests.post(api + "setDeviceSnapEnhanced",
                        data=json.dumps(data),
                        headers=headers)
    print(res.json())
    response = res.json()
    if response['result']['code'] == "0":
        return [i['deviceid'] for i in response['result']['data']['deviceList']]
    else:
        return False


def get_live_list():
    """
    获取直播列表
    :return: 
    """
    data['params'] = {
        "token": accessToken,
        "queryRange": "1-10"
    }
    res = requests.post(api + "liveList",
                        data=json.dumps(data),
                        headers=headers)
    # print(res.text)
    response = res.json()
    print(response)
    if response['result']['code'] == "0":
        return True
    else:
        return False


def create_live(device_id):
    """
    创建设备源直播地址
    :return: 直播封面链接和视频
    """
    data['params'] = {
        "token": accessToken,
        "deviceId": device_id,
        "channelId": 0,
        "streamId": 1,
        "liveMode": "proxy"
    }
    res = requests.post(api + "bindDeviceLiveHttps",
                        data=json.dumps(data),
                        headers=headers)
    response = res.json()
    print(response)
    if response['result']['code'] == "0":
        return response['result']['data']['streams']
    else:
        return False


def delete_live(liveToken):
    """
    删除直播地址
    :return: 直播封面链接和视频
    """
    data['params'] = {
        "token": accessToken,
        "liveToken": liveToken,
    }
    res = requests.post(api + "unbindLive",
                        data=json.dumps(data),
                        headers=headers)
    # print(res.text)
    response = res.json()
    print(response)
    if response['result']['code'] == "0":
        return True
    else:
        return False


def query_live_status(liveToken):
    """
    查询直播状态
    :return: 是否在直播
    """
    data['params'] = {
        "token": accessToken,
        "liveToken": liveToken,
    }
    res = requests.post(api + "queryLiveStatus",
                        data=json.dumps(data),
                        headers=headers)
    response = res.json()
    print(response)
    if response['result']['code'] == "0":
        """
        状态，
        0:正在直播中,
        1:正在直播中，但是视频封面异常,
        2:视频源异常,
        3:码流转换异常,
        4:云存储访问异常,
        5:直播未开始,
        10:直播暂停中,
        11:设备离线(视频源是设备device才会有这个状态)
        """
        return not response['result']['data']['status']
    else:
        return None


def modify_live_status(liveToken, status):
    """
    修改直播状态
    :return: 是否成功
    """
    data['params'] = {
        "token": accessToken,
        "liveToken": liveToken,
        "status": status
    }
    res = requests.post(api + "modifyLivePlanStatus",
                        data=json.dumps(data),
                        headers=headers)
    # print(res.text)
    response = res.json()
    print(response)
    if response['result']['code'] == "0":
        return True
    else:
        return False


def open_live(liveToken):
    # 开启直播
    return modify_live_status(liveToken, True)


def close_live(liveToken):
    # 关闭直播
    return modify_live_status(liveToken, False)


def control_move_ptz_op(device_id):
    """
    生成一个可以控制设备的移动的类
    :return: Op类
    """
    # 设置默认移动持续时间为1.5秒
    duration = 0.5
    op_methods = {
        0: "up",  # 上
        1: "down",  # 下
        2: "left",  # 左
        3: "right",  # 右
        4: "lu",  # 左上
        5: "ld",  # 左下
        6: "ru",  # 右上
        7: "rd",  # 右下
        8: "enlarge",  # 放大
        9: "reduce",  # 缩小
        10: "pause"  # 暂停
    }
    op_data = deepcopy(data)
    op_data['params'] = {
        "token": accessToken,
        "deviceId": device_id,
        "channalId": 0,
        "duration": duration
    }

    def method(code):
        if code in op_methods:
            op_data["operation"] = op_methods[code]
            res = requests.post(api + "controlMovePTZ",
                                data=json.dumps(data),
                                headers=headers)
            # print(res.text)
            response = res.json()
            print(response)
            if response['result']['code'] == "0":
                return True
            else:
                return False
        else:
            return False

    return type("Op", (object,), {v: lambda: method(k) for k, v in op_methods.items()})


if __name__ == "__main__":
    get_live_list()
