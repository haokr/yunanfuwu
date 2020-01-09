# -*- coding: utf-8 -*-
'''
 * @Author: WangHao
 * @Date: 2019-12-29 13:16:31
 * @LastEditors: WangHao
 * @LastEditTime: 2020-01-09 21:03:41
 * @Description: None
'''
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

import redis

redis_cli = redis.Redis(host='localhost', port=6379, db=0)