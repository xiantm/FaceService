from flask import Blueprint, request, jsonify
import face_recognition

facetest = Blueprint('facetest',__name__)


@facetest.route('/detect')
def detect():
    file = request.files['file']
    if file is None:
        return jsonify(msg='find no picture', is_error=False, data={'face_size': 0, 'face':[]})
    img = face_recognition.load_image_file(file)
    locations = face_recognition.face_locations(file)
    landmarks = face_recognition.face_landmarks(img, locations)
    face = []
    for i in range(0,len(locations)):
        face.append({'location': locations[i], 'landmark': landmarks[i]})