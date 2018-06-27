from flask import request, Blueprint, jsonify, render_template
from app.utils import get_face_encode
import uuid
import requests
import os
import face_recognition

yryp = Blueprint('yryp', __name__)


@yryp.route('/')
def index():
    return render_template('demo.html')


@yryp.route('/detect', methods=['POST'])
def detect():
    """
    :param: url 图片url
    :return: {msg，ret(0有人脸特征码，1无人脸特征码)，face_size:人脸数}}
    """
    url = request.args.get('url') or request.form['url']
    if url is None or url == '':
        return jsonify(msg='image url must be not null', ret=1, face_size=0)
    filename = str(uuid.uuid4())
    with open(filename, 'wb') as f:
        try:
            f.write(requests.get(url, timeout=1).content)
        except :
            os.remove(filename)
            return jsonify(msg='image url is invalid', ret=1, face_size=0)
    face_list = get_face_encode(filename)
    os.remove(filename)
    if len(face_list) == 0:
        return jsonify(msg='find no faces', ret=1, face_size=0)
    return jsonify(msg='ok', ret=0, face_size=len(face_list))


@yryp.route('/match', methods=['POST'])
def match():
    """
    :url1: 图片1
    :url2: 图片2
    :tolerance: 通过差值
    :return: {msg,ret:(1，路径非图片或图片里没人脸，0路径可用)，match：人脸是否匹配}
    """
    url1 = request.args.get('url1') or request.form['url1']
    url2 = request.args.get('url2') or request.form['url2']
    tol = request.args.get('tolerance') or request.form['tolerance'] or '0.4'
    tolerance = float(tol)
    if (url1 is None or url1 == '') and (url2 is None or url2 == ''):
        return jsonify(msg='2 url must be not null', ret=1, match=False)
    image1 = str(uuid.uuid4())
    image2 = str(uuid.uuid4())
    with open(image1, 'wb') as f:
        try:
            f.write(requests.get(url1, timeout=1).content)
        except:
            os.remove(image1)
            return jsonify(msg='url1 is invalid', ret=1, match=False)
    face_list1 = get_face_encode(image1)
    os.remove(image1)
    if len(face_list1) == 0:
        return jsonify(msg='url1 find no face', ret=1, match=False)
    with open(image2, 'wb') as f:
        try:
            f.write(requests.get(url2, timeout=1).content)
        except:
            os.remove(image2)
            return jsonify(msg='url2 is invalid', ret=1, match=False)
    face_list2 = get_face_encode(image2)
    os.remove(image2)
    if len(face_list2) == 0:
        return jsonify(msg='url2 find no face', ret=1, match=False)
    for face in face_list1:
        match_result = face_recognition.compare_faces(face_list2, face, tolerance)
        for mr in match_result:
            if mr:
                return jsonify(msg='ok', ret=0, match=True)
    return jsonify(msg='ok', ret=0, match=False)
