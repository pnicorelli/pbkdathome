import os

class Config:
    SALT = os.environ.get('SALT', 'salt_missing').encode('utf-8')
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000