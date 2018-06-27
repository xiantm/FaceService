from app import app
from flask import jsonify
from app.routes.root import root
from app.routes.face_test import facetest
from app.routes.face import face
from app.routes.yryp import yryp

app.register_blueprint(facetest, url_prefix='/facetest')
app.register_blueprint(face, url_prefix='/face')
app.register_blueprint(yryp, url_prefix='/yryp')
app.register_blueprint(root)


@app.errorhandler(400)
def bad_request(e):
    return jsonify(msg='bad request, check your params', ret=400)


@app.errorhandler(500)
def server_error(e):
    return jsonify(msg='sorry,server error', ret=500)
