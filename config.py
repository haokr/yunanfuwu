import os 
from datetime import timedelta

# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'yunanfuwu'
HOST = '139.196.94.212'
PORT = '3306'
DATABASE = 'yunan_dev'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

# 最大上传文件大小 16M
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# jsonify 返回数据中文显示
JSON_AS_ASCII = False

# session 过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days = 1)


SESSION_TYPE = 'filesystem'

SECRET_KEY = os.urandom(24)
