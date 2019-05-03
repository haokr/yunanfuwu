from flask import Blueprint 

monitor = Blueprint('monitor', __name__) 

from . import urls 