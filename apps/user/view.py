from flask import request

def root():
    return 'This is root of user\nIP: '+request.remote_addr