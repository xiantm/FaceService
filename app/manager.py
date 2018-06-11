import face_recognition
import numpy as np
from flask import json
from config import image_path, ip, port
import os
from os import path
from datetime import datetime
from app.models import Face
from app import db

face_cache = []


def compare_1_1(source, target, tolerance):
    """
    将两张图片进行对比
    :param source: 原图片
    :param target: 目标图片
    :param tolerance: 图片差值
    :return: 是否对比成功,信息
    """
    source_data = face_recognition.load_image_file(source)
    source_face = face_recognition.face_encodings(source_data)
    if len(source_face) <= 0:
        return False, "no face in source file"
    target_data = face_recognition.load_image_file(target)
    target_face = face_recognition.face_encodings(target_data)
    if len(target_face) <= 0:
        return False, "no face in target file"
    for unknown_face in target_face:
        match_result = face_recognition.compare_faces(source_face, unknown_face, tolerance)
        for result in match_result:
            if result:
                return True, "matching"
    return False, "mismatch"


def validate_img(face_stream):
    """
    验证人脸图片
    :param face_stream:
    :return: 人脸特征,人脸数
    """
    img = face_recognition.load_image_file(face_stream)
    face_list = face_recognition.face_encodings(img)
    if len(face_list) > 0:
        return len(face_list)
    else:
        return  0


def add_face(file, name=None, group_id=0):
    """
    添加图片到库里
    :param file: 文件
    :param name: 文件对应人名
    :param group_id: 组ID
    :return: 是否添加成功,人脸数
    """
    file_name = str(datetime.now().microsecond) + "." + file.filename.split(".")[1]
    file_path = path.join(image_path, file_name)
    file.save(file_path)
    img = face_recognition.load_image_file(file_path)
    face_list = face_recognition.face_encodings(img)
    face_size = len(face_list)
    if face_size <= 0:
        os.remove(file_path)
        return False, 0
    face_encode = json.dumps([face.tolist() for face in face_list])
    face = Face(file_name=file_name, name=name, create_time=datetime.now(),faces=face_list,
                group_id=group_id, face_size=face_size, face_encode=face_encode)
    face_cache.append(face)
    # db.session.add(face)
    # db.session.commit()
    return True, face_size


def exists(file, group_id, tolerance):
    """
    验证人脸是否存在
    :param file:
    :param group_id:
    :return:
    """
    img = face_recognition.load_image_file(file)
    face_list = face_recognition.face_encodings(img)
    if len(face_list) == 0:
        return False, "find no face in upload file", None, None, None
    face_in_cache = []
    if group_id:
        face_in_cache = list(filter(lambda face: face.group_id == group_id, face_cache))
    else:
        face_in_cache = face_cache
    if len(face_in_cache) == 0:
        return False, "group_id '{}' has no face".format(group_id), None, None, None
    for unknown_face in face_list:
        for face in face_in_cache:
            match_res = face_recognition.compare_faces(face.faces, unknown_face, tolerance)
            for res in match_res:
                if res:
                    return True, "success", "http://{}:{}/static/image/{}".format(ip, port, face.file_name),\
                           face.name, face.face_size
    return False, "not find", None, None, None


def find_all(file, group_id, tolerance):
    """
    找出所有人脸
    :param file:
    :param group_id:
    :return:
    """
    face_result = []
    img = face_recognition.load_image_file(file)
    face_list = face_recognition.face_encodings(img)
    if len(face_list) == 0:
        return False, "find no face in upload file", face_result
    face_in_cache = []
    if group_id:
        face_in_cache = list(filter(lambda face: face.group_id == group_id, face_cache))
    else:
        face_in_cache = face_cache
    if len(face_in_cache) == 0 :
        return False, "group_id '{}' has no face".format(group_id), face_result
    for unknown_face in face_list:
        for face in face_in_cache:
            match_res = face_recognition.compare_faces(face.faces, unknown_face, tolerance)
            for res in match_res:
                if res:
                    face_result.append({"file_path": "http://{}:{}/static/image/{}".format(ip,port,face.file_name),
                                        "name": face.name, "face_size": face.face_size})
    return True, "find {} face".format(len(face_result)), face_result
