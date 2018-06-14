import face_recognition
from flask import json
from app import db
import numpy as np

face_cache = {}

'''存放图片的根路径,docker run -v 挂载地址
'''
root_path = '/root/face/image'


def load_img(project_id, face_list):
    """将数据库中图片路径加载到内存
    :param face_list: 预加载数据
    :param root_path:  根路径
    :param project_id:  活动ID
    :return True 加载成功,False 加载失败
    """
    # 清除内存中的数据
    manager = FaceRecognitionManger(project_id)
    face_cache[project_id] = manager
    for item in face_list:
        if item.face_encode is not None and len(item.face_encode) > 0:
            item.faces = [np.array(face) for face in json.loads(item.face_encode)]
        else:
            if item.sold_face_photo is not None and len(item.sold_face_photo) > 0:
                try:
                    image = face_recognition.load_image_file(root_path + "/" + project_id + "/" + item.sold_face_photo)
                    item.faces = face_recognition.face_encodings(image)
                    item.face_encode = json.dumps([face.tolist() for face in item.faces])
                    db.session.add(item)
                    db.session.commit()
                except:
                    print("File Not Found")
        manager.faceList.append(item)


def face_compare_1n(project_id, face_stream, tolerance):
    fm = face_cache.get(project_id)
    if fm:
        return fm.compare_1_n(face_stream, tolerance)
    return False, None, None, "活动号配置错误",None


def face_compare_11(project_id, face_stream, sold_id, tolerance):
    fm = face_cache.get(project_id)
    if fm:
        return fm.compare_1_1(face_stream, sold_id, tolerance)
    return False, None, None, "活动号配置错误"


def validate_img(face_stream):
    """
    验证人脸
    :param face_stream:
    :return: 人脸特征，识别出的人脸数目
    """
    img = face_recognition.load_image_file(face_stream)
    face_list = face_recognition.face_encodings(img)
    if len(face_list) > 0:
        return json.dumps([face.tolist() for face in face_list]), len(face_list)
    else:
        return None, 0


# 人脸识别器
class FaceRecognitionManger(object):

    def __init__(self, project_id):
        """
        :param project_id 活动号
        """
        # 解码过的人脸集合 item = {'rfid': rfid, 'name': name, 'path': path, 'faces': faces}
        self.faceList = []
        self.project_id = project_id

    def compare_1_n(self, file_stream, tolerance):
        """74：n对比人脸,需要返回人名
        :param file_stream: 识别文件流
        :param tolerance: 识别准确度 (0.74 - 74 )
        :return: (是否对比成功,文件路径,人名,提示信息,sold_id)
        """
        img = face_recognition.load_image_file(file_stream)
        unknown_face = face_recognition.face_encodings(img)
        if len(unknown_face) > 0:
            # 只要有一张脸对比成功就确定对比成功
            for item in self.faceList:
                for item_unknown in unknown_face:
                    match_results = face_recognition.compare_faces(item.faces, item_unknown, tolerance)
                    for item_result in match_results:
                        if item_result:
                            return True, item.sold_face_photo, item.sold_user_name, "人脸对比成功", item.sold_id
        else:
            return False, None, None, "未检测出人脸", None
        return False, None, None, "人脸对比失败", None

    def compare_1_1(self, file_stream, sold_id, tolerance):
        """74：1对比人脸
        :param file_stream: 识别文件流
        :param rfid: 电子标签信息
        :param tolerance: 识别准确度 (0.74 - 74)
        :return: (0对比失败1对比成功2第一次对比3未找到人脸,文件路径,人名,提示信息)
        """
        for item in self.faceList:
            if sold_id == str(item.sold_id):
                img = face_recognition.load_image_file(file_stream)
                unknown_face = face_recognition.face_encodings(img)
                if len(unknown_face) > 0:
                    # 有存留图片就对比存留图片
                    if len(item.faces) > 0:
                        for item_unknown in unknown_face:
                            match_results = face_recognition.compare_faces(item.faces, item_unknown, tolerance)
                            for item_result in match_results:
                                if item_result:
                                    return True, item.sold_face_photo, item.sold_user_name, "人脸对比成功"
                        return False, None, None, "人脸对比失败"
                    # 没有存留图片保存存留图片
                    else:
                        item.faces = unknown_face
                        item.face_encode = json.dumps([encode.tolist() for encode in item.faces])
                        db.session.add(item)
                        db.session.commit()
                        return True, item.sold_face_photo, item.sold_user_name, "人脸已保存"
                else:
                    return False, None, None, "未检测出人脸"
        return False, None, None, "无效票证"
