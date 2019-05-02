from flask import Blueprint, request,session
from apps.user import view

user = Blueprint('user', __name__)

@user.route('/')
def root():
    return view.root()

@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return view.login()
    else:
        return view.getlogin()

@user.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return view.registerPage()
    else:
        return view.register()

@user.route('/child', methods=['GET', 'POST'])
def child():
    if request.method == 'GET':
        return view.showChilds()
    else:
        return view.addChild()

