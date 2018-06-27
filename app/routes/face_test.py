from flask import redirect, Blueprint, request, jsonify
from app.utils import face_detect as detect
from config import image_path
import uuid
import face_recognition
import os
import requests

face_cache = []
images = os.listdir(image_path)
# for image in images:
#     img = face_recognition.load_image_file(image_path + "/" + image)
#     code_list = face_recognition.face_encodings(img)
#     face_cache.append({
#         'id': str(uuid.uuid4()),
#         'file_name': image,
#         # 'file_path': 'http://192.168.0.99:5000/static/image/{}'.format(image),
#         'file_path': '/static/image/{}'.format(image),
#         'code': code_list
#     })
#
facetest = Blueprint('facetest', __name__)


@facetest.route('/')
def index():
    return redirect('/static/test.html')


@facetest.route('/detectbyfile', methods=['POST'])
def detect_by_file():
    file = 'image' in request.files and request.files['image'] or None
    if file is None:
        return jsonify(msg='image must be upload', ret=1, data={'face_size': 0, 'face': []})
    return detect(file)


@facetest.route('/detectbyurl', methods=['POST'])
def detect_by_url():
    url = request.args.get('url') or request.form['url']
    if url is None or url == '':
        return jsonify(msg='image url must be not null', ret=1, data={'face_size': 0, 'face': []})
    filename = str(uuid.uuid4())
    with open(filename, 'wb') as f:
        f.write(requests.get(url, timeout=0.3).content)
    result = detect(filename)
    os.remove(filename)
    return result


@facetest.route('/match', methods=['POST'])
def match():
    image1 = 'image1' in request.files and request.files['image1'] or None
    image2 = 'image2' in request.files and request.files['image2'] or None
    if image1 is None or image2 is None:
        return jsonify(msg='2 image must be upload', ret=3, data={'similarity': 1})
    face_data1 = face_recognition.load_image_file(image1)
    face_list1 = face_recognition.face_encodings(face_data1)
    if len(face_list1) == 0:
        return jsonify(msg='find no face in image1', ret=1, data={'similarity': 1})
    face_data2 = face_recognition.load_image_file(image2)
    face_list2 = face_recognition.face_encodings(face_data2)
    if len(face_list2) == 0:
        return jsonify(msg='find no face in image2', ret=2, data={'similarity': 1})
    # 获取两张照片对比人脸的最小差值
    distance = 1
    for face in face_list1:
        distance_t = face_recognition.face_distance(face_list2, face).min()
        if distance_t < distance:
            distance = distance_t
    return jsonify(msg='ok', ret=0, data={'similarity': distance})


@facetest.route('/matchbyurl', methods=['POST'])
def match_by_url():
    url1 = request.args.get('url1') or request.form['url1']
    url2 = request.args.get('url2') or request.form['url2']
    if (url1 is None or url1 == '') and (url2 is None or url2 == ''):
        return jsonify(msg='2 url must be not null', ret=1, data={'similarity': 0})
    image1 = str(uuid.uuid4())
    image2 = str(uuid.uuid4())
    with open(image1, 'wb') as f:
        f.write(requests.get(url1, timeout=0.3).content)
    with open(image2, 'wb') as f:
        f.write(requests.get(url2, timeout=0.3).content)
    try:
        face_data1 = face_recognition.load_image_file(image1)
        face_list1 = face_recognition.face_encodings(face_data1)
        face_data2 = face_recognition.load_image_file(image2)
        face_list2 = face_recognition.face_encodings(face_data2)
    except:
        return jsonify(msg='url is not picture', ret=1, data={'similarity': 0})
    finally:
        os.remove(image1)
        os.remove(image2)
    # 获取两张照片对比人脸的最小差值
    distance = 1
    for face in face_list1:
        distance_t = face_recognition.face_distance(face_list2, face).min()
        if distance_t < distance:
            distance = distance_t
    return jsonify(msg='ok', ret=0, data={'similarity': distance})


@facetest.route('/images', methods=['GET'])
def images():
    res_list = []
    for item in face_cache:
        res_list.append({
            'id': item['id'],
            'file_name': item['file_name'],
            'file_path': item['file_path']
        })
    return jsonify(res_list)


@facetest.route('/searchbyfile', methods=['POST'])
def search_by_file():
    file = 'image' in request.files and request.files['image'] or None
    if file is None:
        return jsonify(msg='image must be upload', ret=1, data={'candidates': []})
    return search(file)


@facetest.route('/searchbyurl', methods=['POST'])
def search_by_url():
    url = request.args.get('url') or request.form['url']
    if url is None or url == '':
        return jsonify(msg='image url must be not null', ret=1, data={'candidates': []})
    filename = str(uuid.uuid4())
    with open(filename, 'wb') as f:
        f.write(requests.get(url, timeout=0.3).content)
    result = search(filename)
    os.remove(filename)
    return result


def search(file):
    try:
        img = face_recognition.load_image_file(file)
        code_list = face_recognition.face_encodings(img)
        list = []
        if len(code_list) == 0:
            return jsonify(msg='find no face in picture', ret=1, data={'candidates': []})
        for face in face_cache:
            distance = 1
            for code in code_list:
                td = face_recognition.face_distance(face['code'], code).min()
                if td < distance:
                    distance = td
            list.append({
                'id': face['id'],
                'file_name': face['file_name'],
                'file_path': face['file_path'],
                'distance': distance
            })
        return jsonify(msg='ok', ret=0, data={'candidates': list})
    except:
        return jsonify(msg='url is not picture', ret=1, data={'candidates': []})
