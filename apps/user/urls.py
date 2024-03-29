from flask import Blueprint, request,session
from apps.user import view

user = Blueprint('user', __name__)


'''
    Page
'''


# 账号信息展示及修改
@user.route('/edit/<uid>', methods=['GET', 'POST'])
def massage(uid):
    if request.method == 'GET':
        return view.showUser(uid)
    else:
        return view.modifyUser(uid)


# 子账号添加路由
@user.route('/add/<uid>', methods=['GET', 'POST'])
def add(uid):
    if request.method == 'GET':
        return view.showAddUser(uid)
    else:
        return view.addChild(uid)


#子账号删除
@user.route('drop/<cid>', methods=['GET','POST'])
def drop(cid):
    return view.dropchild(cid)


''' 
    API 
'''

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


# 微信用户登陆路由
@user.route('/wxlogin', methods=['POST'])
def wx_login():
    return view.wx_login()
