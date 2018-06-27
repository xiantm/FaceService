import face_recognition
import traceback
from flask import jsonify


def get_face_encode(file, biggest=False):
    """
    获取人脸编码
    :param file:
    :param biggest: 只需要最大的那张脸
    :return:
    """
    try:
        img = face_recognition.load_image_file(file)
        if biggest:
            locations = face_recognition.face_locations(img)
            locations.sort(key=lambda location: (location[2] - location[0]) * (location[1] - location[3]))
            return face_recognition.face_encodings(img, known_face_locations=[locations[0]])
        return face_recognition.face_encodings(img)
    except Exception as e:
        traceback.print_exc()
        return []


def face_detect(file):
    """
    获取人脸特征
    :param file:
    :return:
    """
    img = face_recognition.load_image_file(file)
    try:
        locations = face_recognition.face_locations(img)
        landmarks = face_recognition.face_landmarks(img, locations)
    except:
        return jsonify(msg='url is not picture', ret=1, data={})
    face = []
    for i in range(0, len(locations)):
        face.append({'location': locations[i], 'landmark': landmarks[i]})
    return jsonify(msg='ok', ret=0, data={'face_size': len(locations), 'face': face})


def get_biggest_face_location(file):
    """
    获取最大的人脸矩形
    :param file:
    :return:
    """
    img = face_recognition.load_image_file(file)
    try:
        locations = face_recognition.face_locations(img)
        locations.sort(key=lambda location: (location[2] - location[0]) * (location[1] - location[3]))
        return locations[0]
    except:
        return None
