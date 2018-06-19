import os
basedir = os.path.abspath(os.path.dirname(__file__))
image_path = os.path.join(basedir, "app", "static", "image")
if not os.path.exists(image_path):
    os.mkdir(image_path)
ip = "127.0.0.1"
port = "5000"



class Config(object):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://server_user:server123456@47.98.49.11:3306/gateway_system"
    SQLALCHEMY_TRACK_MODIFICATIONS = False