from app import app
from app.routes.face_test import facetest
from app.routes.root import root


app.register_blueprint(facetest,url_prefix='/facetest')
app.register_blueprint(root)
