from flask import Blueprint, g
import apps.api.view as view

api = Blueprint('api', __name__)

@api.route('/')
def root():
    return view.root()

