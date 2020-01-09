from flask import Flask, jsonify, url_for, render_template, request, abort, redirect, session, g
from werkzeug import secure_filename
from socketIO import socketio
from flask_session import Session
from db import db
import config

from apps.api.urls import api
from apps.equipment.urls import equipment
from apps.data.urls import data
from apps.record.urls import record
from apps.user.urls import user
from apps.monitor.urls import monitor
from apps.role.urls import role
from apps.gov.urls import gov


app = Flask(__name__, static_folder='static')

app.config.from_object(config)

Session(app)
db.init_app(app)
socketio.init_app(app, manage_session=False)

@app.before_request
def before_request():
    user_id = session.get("id")
    ignore = ['/user/login', '/user/register', '/gov/regist', '/gov/login', '/user/wxlogin', '/monitor/wxshow', '']
    isReport = request.path.startswith('/monitor/report/') or request.path.startswith('/monitor/uireport/') 
    isStatic = request.path.startswith('/static')

    if request.path == '/favicon.ico':
    	return redirect('/static/img/yunan_logo_3.png')
    if ( not user_id ) and ( request.path  not in ignore ) and ( not isReport ) and ( not isStatic ):
        return redirect('/user/login')

@app.before_request
def loginedUserClass():
	class_ = session.get('class_')
	if request.path == '/user/login' or request.path == '/gov/login' or request.path.startswith('/static/') or request.path.startswith('/monitor/report/') or request.path.startswith('/monitor/uireport/'):
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

if __name__ == '__main__':
#    app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
    socketio.run(app, debug=True)
