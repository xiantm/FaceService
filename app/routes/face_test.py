from flask import Blueprint, request, jsonify
import face_recognition

facetest = Blueprint('facetest', __name__)


@facetest.route('/detect')
def detect():
    file = request.files['image']
    if file is None:
        return jsonify(msg='you don\'t upload image', ret=1, data={'face_size': 0, 'face': []})
    img = face_recognition.load_image_file(file)
    locations = face_recognition.face_locations(file)
    landmarks = face_recognition.face_landmarks(img, locations)
    face = []
    for i in range(0, len(locations)):
        face.append({'location': locations[i], 'landmark': landmarks[i]})
    return jsonify(msg='ok', ret=0, data={'face_size': len(locations), 'face': face})


@facetest.route('/match')
def match():
    image1 = request.files['image1']
    image2 = request.files['image2']
    if image1 is None or image2 is None:
        return jsonify(msg='you don\'t upload two image', ret=1, data={'similarity': 0, 'face': []})
