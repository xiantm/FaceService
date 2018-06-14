import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@db:3306/gateway_system"
    SQLALCHEMY_TRACK_MODIFICATIONS = False