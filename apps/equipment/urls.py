from flask import Blueprint
import apps.equipment.view as view

equipment = Blueprint('equipment', __name__)

@equipment.route('/')
def root():
    return view.root()