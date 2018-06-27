from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_cors import *

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)

# 防止循环导入
from app import models, routes
