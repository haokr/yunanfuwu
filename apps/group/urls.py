from flask import Blueprint
from apps.group import view

group = Blueprint('group', __name__)

@group.route('/')
def root():
    return view.root()