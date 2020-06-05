from flask import Flask, request, abort, redirect, session
from flask_session import Session

import config
from apps.api.urls import api
from apps.data.urls import data
from apps.equipment.urls import equipment
from apps.gov.urls import gov
from apps.live.urls import live
from apps.monitor.urls import monitor
from apps.record.urls import record
from apps.role.urls import role
from apps.user.urls import user
from db import db
from socketIO import socketio

app = Flask(__name__, static_folder='static')

app.config.from_object(config)

Session(app)
db.init_app(app)
socketio.init_app(app, manage_session=False)


@app.before_request
def before_request():
    user_id = session.get("id")
    ignore = ['/user/login', '/user/register', '/gov/regist', '/gov/login', '/user/wxlogin', '/monitor/wxshow', '/monitor/reportonphone', '']
    isReport = request.path.startswith('/monitor/report/') or request.path.startswith('/monitor/uireport/')
    isStatic = request.path.startswith('/static')
    isGetHeartbeat = "/equipment/heartbeat/e_"

    if request.path == '/favicon.ico':
        return redirect('/static/img/yunan_logo_3.png')
    if (not user_id) and (request.path.lower() not in ignore) and (not isReport) and (not isStatic) and (not isGetHeartbeat):
        return redirect('/user/login')


@app.before_request
def loginedUserClass():
    class_ = session.get('class_')
    if request.path == '/user/login' \
            or request.path == '/gov/login' \
            or request.path.startswith('/static/') \
            or request.path.startswith('/monitor/report/') \
            or request.path.startswith('/monitor/uireport/')\
            or request.path.lower().startswith('/monitor/reportonphone/') \
            or request.path.startswith('/equipment/heartbeat/e_'):
        pass
    elif class_ == 'user' and request.path.startswith('/gov/'):
        return abort(404)
    elif class_ == 'gov' and not request.path.startswith('/gov/'):
        return abort(404)


# blueprint
app.register_blueprint(equipment)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(equipment, url_prefix='/equipment')
app.register_blueprint(record, url_prefix='/record')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(monitor, url_prefix='/monitor')
app.register_blueprint(data, url_prefix='/data')
app.register_blueprint(role, url_prefix='/role')
app.register_blueprint(gov, url_prefix='/gov')
app.register_blueprint(live, url_prefix='/live')

if __name__ == '__main__':
    #    app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
    socketio.run(app, debug=True)
