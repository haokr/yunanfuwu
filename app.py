from flask import Flask, jsonify, url_for, render_template, request, abort, redirect, session, g
from werkzeug import secure_filename
from socketIO import socketio
from flask_session import Session
from db import db
from models import User, User_record, Group, Equipment, Alarm_record
import config

from apps.api.urls import api
from apps.equipment.urls import equipment
from apps.group.urls import group
from apps.record.urls import record
from apps.user.urls import user
from apps.monitor.urls import monitor

app = Flask(__name__)

app.config.from_object(config)

Session(app)
db.init_app(app)
socketio.init_app(app, manage_session=False)


@app.before_request
def before_request():
    user_id = session.get("id")
    ignore = ['/user/login', '/user/register']
    isReport = request.path.startswith('/monitor/report/')
    if not user_id and request.path not in ignore and not isReport:
        return redirect('/user/login')

# blueprint
app.register_blueprint(equipment)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(equipment, url_prefix='/equipment')
app.register_blueprint(group, url_prefix='/group')
app.register_blueprint(record, url_prefix='/record')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(monitor, url_prefix='/monitor')



if __name__ == '__main__':
    socketio.run(app)