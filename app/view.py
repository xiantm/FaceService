from app import app
from app.routes.face_test import facetest


app.register_blueprint(facetest, "/facetest")