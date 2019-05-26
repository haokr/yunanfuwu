from flask import Flask, jsonify, url_for, render_template, request, abort, redirect, session, g
from werkzeug import secure_filename
from socketIO import socketio
from flask_session import Session
from db import db
from models import User, User_record, Group, Equipment, Alarm_record
import config

from apps.api.urls import api
from apps.equipment.urls import equipment
from apps.data.urls import data
from apps.record.urls import record
from apps.user.urls import user
from apps.monitor.urls import monitor
from apps.role.urls import role


app = Flask(__name__, static_folder='static')

app.config.from_object(config)

Session(app)
db.init_app(app)
socketio.init_app(app, manage_session=False)


@app.before_request
def before_request():
    user_id = session.get("id")
    ignore = ['/user/login', '/user/register']
    isReport = request.path.startswith('/monitor/report/')
    isStatic = request.path.startswith('/static')
    if ( not user_id ) and ( request.path  not in ignore ) and ( not isReport ) and ( not isStatic ):
        return redirect('/user/login')


# blueprint
app.register_blueprint(equipment)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(equipment, url_prefix='/equipment')
app.register_blueprint(record, url_prefix='/record')
app.register_blueprint(user, url_prefix='/user')
app.register_blueprint(monitor, url_prefix='/monitor')
app.register_blueprint(data, url_prefix='/data')
app.register_blueprint(role, url_prefix='/role')


if __name__ == '__main__':
    socketio.run(app)