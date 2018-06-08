import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://server_user:server123456@47.98.49.11:3306/gateway_system"
    SQLALCHEMY_TRACK_MODIFICATIONS = False