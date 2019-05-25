from flask import Blueprint, request,session
from apps.role import view

role = Blueprint('role', __name__)


# 角色信息展示及修改
@role.route('/show/<rid>', methods=['GET', 'POST'])
def massage(rid):
    if request.method == 'GET':
        return view.showRole(rid)
    else:
        return view.modifyRole(rid)


# 用户添加角色
@role.route('/addrole/<rid>', methods=['GET', 'POST'])
def use(rid):
    return view.addRole(rid)


# 展示用户创建的角色及添加角色
@role.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return view.getRoles()
    else:
        return view.Roleadd()