from flask import Blueprint
from apps.record import view

record = Blueprint('record', __name__)

@record.route('/')
def root():
    return view.root()


@record.route('/data')
def data_record():
    return view.data_record()


@record.route("/ui")
def ui_record():
    return view.ui_record()