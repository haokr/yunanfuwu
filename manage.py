
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from db import db

manager = Manager(app)

# 1. 要使用 flask-migrate 必须要绑定 app 和 db
migrate = Migrate(app, db)
# 2. 把 MigrateCommand 命令添加到 manager 中
# 模型 -> 迁移文件 -> 表
# init -> migrate -> upgrade
# 修改数据表字段，直接从 migrate 开始执行即可
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()