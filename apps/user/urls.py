from flask import Blueprint, request,session
from apps.user import view

user = Blueprint('user', __name__)


# 初始路由
@user.route('/')
def root():
    return view.root()


# 用户登陆路由
@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return view.login()
    else:
        return view.getlogin()


# 登出路由
@user.route('/logout', methods=['POST'])
def logout():
    return view.logout()


# 注册路由
@user.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return view.registerPage()
    else:
        return view.register()


# 子账号信息展示路由
@user.route('/child', methods=['GET', 'POST'])
def child():
    if request.method == 'GET':
        return view.showChilds()
    else:
        return view.addChild()


