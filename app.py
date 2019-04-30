from flask import Flask, jsonify, url_for, render_template, request, abort, redirect, session
from werkzeug import secure_filename
from db import db
from models import User, User_record, Group, Equipment, Alarm_record
import config

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)

app.debug = True

if __name__ == '__main__':
    app.run()