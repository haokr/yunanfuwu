from flask import Blueprint
from apps.user import view

user = Blueprint('user', __name__)

@user.route('/')
def root():
    return view.root()
