from flask import request, session, jsonify, render_template, url_for, redirect


def devices():
    devices_ = [{'name': 'test1', 'href': "#"}]
    return render_template('live/devices.html', {'devices': })


def living(sid):
    pass
