from config import image_path
import os
import face_recognition
from app.models import Face
import uuid
from app import db
import numpy as np
import json

cache = []

face_cache = []

# 测试数据
images = os.listdir(image_path)
for image in images:
    img = face_recognition.load_image_file(image_path + "/" + image)
    code_list = face_recognition.face_encodings(img)
    cache.append(Face(id=str(uuid.uuid4()), faces=code_list, group_id='youwillneveruse', face_size=len(code_list)))

# 恢复数据
face_list = Face.query.all()
for item in face_list:
    item.faces = [np.array(face) for face in json.loads(item.face_encode)]
    cache.append(item)


def add(face):
    """
    添加人脸
    :param face: Face
    """
    cache.append(face)
    db.session.add(face)
    db.session.commit()


def del_face(face_id):
    """
    通过ID删除人脸
    :param face_id: 人脸ID
    :return:
    """
    filter_list = list(filter(lambda f: f.id == face_id, cache))
    if len(filter_list) == 0:
        return False
    db.session.delete(filter_list[0])
    db.session.commit()
    cache.remove(filter_list[0])
    return True


def clear_cache():
    for face in face_cache:
        db.session.delete(face)
    db.session.commit()
    cache.clear()


def get_all():
    """
    获取所有人脸
    :return:
    """
    return cache


def get_group(group_id):
    """
    获取某个组的人脸
    :param group_id:
    :return:
    """
    return list(filter(lambda f: f.group_id == group_id, cache))
