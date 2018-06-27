from flask import render_template, request, jsonify, Blueprint
from app import app, manager

root = Blueprint('root', __name__)


@root.route('/')
def hello_world():
    return render_template("index.html")


@root.route('/f/add', methods=['POST'])
def face_add():
    group_id = request.args.get("group_id") or request.form["group_id"]
    file = request.files['file']
    name = request.args.get("name") or request.form["name"]
    if file is None:
        return jsonify({"status": False, "message": '请求缺少图片文件'})
    status, face_size = manager.add_face(file, name, group_id)
    return jsonify(status=status, message="find {} face".format(face_size))


@root.route('/f/exists', methods=['POST'])
def face_exists():
    """
    :param group_id 活动号
    :param tolerance 识别精度0.1-1越小越准确
    :param file 需要对比的图片
    :return: {"status": status, "file_path": 图片地址, "name": 用户姓名, "message": message}
    """
    group_id = request.args.get("group_id") or request.form["group_id"]
    tol = request.args.get('tolerance') or request.form['tolerance'] or '0.25'
    tolerance = float(tol)
    face = request.files['file']
    if face is None:
        return jsonify(status=False, message='请求缺少图片文件', file_path="", name="", file_size="")
    status, message, file_name, name, file_size = manager.exists(face, group_id, tolerance)
    return jsonify(status=status, message=message, file_path=file_name, name=name, file_size=file_size)


@root.route('/f/findall', methods=['POST'])
def face_find_all():
    """
    判断图片的人脸是否存在
    :param group_id 组号
    :param tolerance 识别精度0.1-1越小越准确
    :param file 需要对比的图片
    :return: {"status": status, file_path: 图片路径, "name": 用户姓名,face_size:人脸数, "message": message}
    """
    group_id = request.args.get("group_id") or request.form["group_id"]
    tol = request.args.get('tolerance') or request.form['tolerance'] or '0.25'
    tolerance = float(tol)
    face = request.files['file']
    if face is None:
        return jsonify(status=False, message='请求缺少图片文件', data = [])
    status, message, data = manager.find_all(face, group_id, tolerance)
    return jsonify(status=status, message=message, data=data)


@root.route('/f/compare/11', methods=['POST'])
def face_compare_11():
    """
    :param tolerance 识别精度0.1-1越小越准确
    :param source 原图片
    :param target 需要对比的图片
    :return: {"status": status, "image": 图片名称, "name": 用户姓名, "message": message}
    """
    tol = request.args.get('tolerance') or request.form['tolerance'] or '0.25'
    tolerance = float(tol)
    source = request.files['source']
    target = request.files['target']

    if source is None or target is None:
        return jsonify({"status": -1, "message": '请求缺少图片文件,必须上传两张图片'})
    status, message = manager.compare_1_1(source, target, tolerance)
    return jsonify(status=status, message=message)


@root.route('/f/validate', methods=['POST'])
def face_validate():
    """
    :param file 需要对比的图片
    :return: {"status": status,"message": message,'face_size': 人脸数}
    """
    face = request.files['file']
    if face is None:
        return jsonify({"status": -1, "message": '请求缺少图片文件'})
    face_size = manager.validate_img(face)
    if face_size > 0:
        return jsonify({
            'status': '1',
            'face_size': face_size,
            'message': 'success',
        })
    return jsonify({
        'status': '0',
        'face_size': '0',
        'message': 'fail',
    })
