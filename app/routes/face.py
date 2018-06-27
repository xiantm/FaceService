from flask import request, Blueprint, jsonify, json
from datetime import datetime
from app.utils import get_face_encode, face_detect
from app import face_cache
from app.models import Face
import uuid
import requests
import os
import face_recognition

face = Blueprint('face', __name__)


@face.route('/add', methods=['POST'])
def add():
    """
    :param group_id 组ID，用户自定义字符串
    :param url 图片url
    :return: { msg:,ret(0添加成功，1添加失败)，data:{face_size,face_id}}
    """
    group_id = request.args.get('group_id')
    url = request.args.get('url')
    if url is None or url == '':
        return jsonify(msg='image url must be not null', ret=1, data={'face_size': 0, 'face_id': None})
    filename = str(uuid.uuid4())
    with open(filename, 'wb') as f:
        try:
            f.write(requests.get(url, timeout=2).content)
        except:
            os.remove(filename)
            return jsonify(msg='image url is invalid', ret=1, data={'face_size': 0, 'face_id': None})
    face_list = get_face_encode(filename)
    os.remove(filename)
    if len(face_list) == 0:
        return jsonify(msg='find no face', ret=1, data={'face_size': 0, 'face_id': None})
    face_id = str(uuid.uuid4())
    face_encode = json.dumps([f.tolist() for f in face_list])
    face_item = Face(id=face_id, face_encode=face_encode, create_time=datetime.now(), face_size=len(face_list),
                     group_id=group_id, faces=face_list, face_url=url)
    face_cache.add(face_item)
    return jsonify(msg='ok', ret=0, data={'face_size': len(face_list), 'face_id': face_item.id})


@face.route('/delete', methods=['POST'])
def delete_face():
    """
    删除人脸
    :param face_ids 人脸ID集合，分隔符|
    :return: {msg,ret=0操作成功}
    """
    face_ids = request.args.get('face_ids')
    for face_id in face_ids.split('|'):
        face_cache.del_face(face_id=face_id)
    return jsonify(msg='ok', ret=0)


@face.route('/deleteAll', methods=['POST'])
def delete_all():
    """
    删除全部
    :return: {msg,ret=0操作成功}
    """
    face_cache.clear_cache()
    return jsonify(msg='ok', ret=0)


@face.route('/detect', methods=['POST'])
def detect():
    """
    :param url 图片url
    :return: { msg:,ret(0成功，1失败)，data:{face_size人脸数,face人脸特征集合}}
    """
    url = request.args.get('url')
    if url is None or url == '':
        return jsonify(msg='image url must be not null', ret=1, data={'face_size': 0, 'face': []})
    filename = str(uuid.uuid4())
    with open(filename, 'wb') as f:
        try:
            f.write(requests.get(url, timeout=2).content)
        except:
            os.remove(filename)
            return jsonify(msg='image url is invalid', ret=1, data={'face_size': 0, 'face': []})
    result = face_detect(filename)
    os.remove(filename)
    return result


@face.route('/match', methods=['POST'])
def match():
    """
    对比两张图片
    :url1: 图片1
    :url2: 图片2
    :return: {msg,ret:(1，路径非图片或图片里没人脸，0路径可用)，distance：人脸差值}
    """
    distance = 1
    url1 = request.args.get('url1')
    url2 = request.args.get('url2')
    match_biggest_face = request.args.get('match_biggest_face', 'false')
    if (url1 is None or url1 == '') and (url2 is None or url2 == ''):
        return jsonify(msg='2 url must be not null', ret=1, distance=distance)
    image1 = str(uuid.uuid4())
    image2 = str(uuid.uuid4())
    with open(image1, 'wb') as f:
        try:
            f.write(requests.get(url1, timeout=2).content)
        except:
            os.remove(image1)
            return jsonify(msg='url1 is invalid', ret=1, distance=distance)
    if match_biggest_face == 'true':
        face_list1 = get_face_encode(image1, True)
    else:
        face_list1 = get_face_encode(image1)
    os.remove(image1)
    if len(face_list1) == 0:
        return jsonify(msg='url1 find no face', ret=1, distance=distance)
    with open(image2, 'wb') as f:
        try:
            f.write(requests.get(url2, timeout=2).content)
        except:
            os.remove(image2)
            return jsonify(msg='url2 is invalid', ret=1, distance=distance)
    if match_biggest_face == 'true':
        face_list2 = get_face_encode(image2, True)
    else:
        face_list2 = get_face_encode(image2)
    os.remove(image2)
    if len(face_list2) == 0:
        return jsonify(msg='url2 find no face', ret=1, distance=distance)
    for face_item in face_list1:
        distance_t = face_recognition.face_distance(face_list2, face_item).min()
        if distance_t < distance:
            distance = distance_t
    return jsonify(msg='ok', ret=0, distance=distance)


@face.route('/search', methods=['POST'])
def search():
    """
    :param group_id: 组id
    :param url: 需要识别图片url
    :param max_distance: 最大差值
    :return:    ret	是	int	返回码； 0表示成功，非0表示出错
                msg	是	string	返回信息；ret非0时表示出错时错误原因
                data	是	object	返回数据；ret为0时有意义
                + group_size	是	int	本次识别请求检索的库总大小
                + face_list
                    + face_id
                    + distance
    """
    group_id = request.args.get('group_id')
    max_distance = float(request.args.get('max_distance'))
    url = request.args.get('url')
    if url is None or url == '':
        return jsonify(msg='url must be not null', ret=1, data={})
    filename = str(uuid.uuid4())
    with open(filename, 'wb') as f:
        try:
            f.write(requests.get(url, timeout=2).content)
        except:
            os.remove(filename)
            return jsonify(msg='image url is invalid', ret=1, data={})
    unknown_face_list = get_face_encode(filename)
    if len(unknown_face_list) == 0:
        return jsonify(msg='image has no face', ret=1, data={})
    face_list = []
    os.remove(filename)
    known_face_list = face_cache.get_group(group_id)
    # 获取小于最大差值的人脸
    for face_item in known_face_list:
        temp_distance = 1
        for unknown_face in unknown_face_list:
            min_distance = face_recognition.face_distance(face_item.faces, unknown_face).min()
            if min_distance <= temp_distance:
                temp_distance = min_distance
        if temp_distance <= max_distance:
            face_list.append({'face_id': face_item.id, 'distance': min_distance})
    return jsonify(msg='ok', ret=0, data={'group_size': len(known_face_list), 'face_list': face_list})
