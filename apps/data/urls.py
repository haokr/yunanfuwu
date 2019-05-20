from flask import Blueprint, g
import apps.data.view as view

data = Blueprint('data', __name__)

@data.route('/')
def root():
    return view.dataPage()

@data.route('/base')
def baseData():
    return view.baseData()

