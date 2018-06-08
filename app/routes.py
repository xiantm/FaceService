from flask import render_template, request, jsonify
from app import app, face_recognition_manager
from app.models import Face


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/face/load')
def load_face():
    """ 加载活动图片信息到内存
    :param project_id 活动号
    :return {status:1成功、0失败,message:...}
    """
    project_id = request.args.get("project_id") or request.form["project_id"]
    if len(project_id) < 1:
        return "fail, give me project_id please "
    face_list = Face.query.filter_by(ticket_project_id=project_id).all()
    if len(face_list) > 0:
        face_recognition_manager.load_img(project_id, face_list)
        return jsonify({'status': 1, 'message': 'success'})
    return jsonify({'status': 0, 'message': 'fail, not find data in this project'})


@app.route('/face/compare/1n', methods=['POST'])
def face_compare_1n():
    """
    :param project_id 活动号
    :param tolerance 识别精度0.1-1越小越准确
    :param file 需要对比的图片
    :return: {"status": status, "image": 图片名称, "name": 用户姓名, "message": message, "sold_id": sold_id}
    """
    project_id = request.args.get("project_id") or request.form["project_id"]
    tol = request.args.get('tolerance') or request.form['tolerance'] or '0.25'
    tolerance = float(tol)
    face = request.files['file']
    (status, file_path, name, message,sold_id) = face_recognition_manager.face_compare_1n(project_id, face, tolerance)
    return jsonify({"status": status, "image": file_path, "name": name, "message": message, "sold_id": sold_id})


@app.route('/face/compare/11', methods=['POST'])
def face_compare_11():
    """
    :param project_id 活动号
    :param tolerance 识别精度0.1-1越小越准确
    :param file 需要对比的图片
    :param rfid m1卡号
    :return: {"status": status, "image": 图片名称, "name": 用户姓名, "message": message}
    """
    project_id = request.args.get('project_id') or request.form["project_id"]
    if project_id == '' or project_id is None:
        return jsonify({"status": -1, "message": '请求缺少project_id'})
    tol = request.args.get('tolerance') or request.form['tolerance'] or '0.25'
    tolerance = float(tol)
    rfid = request.args.get('rfid') or request.form['rfid']
    if rfid == '' or rfid is None:
        return jsonify({"status": -1, "message": '请求缺少rfid'})
    face = request.files['file']
    if face is None:
        return jsonify({"status": -1, "message": '请求缺少图片文件'})
    (status, file_path, name, message) = face_recognition_manager.face_compare_11(project_id, face, rfid, tolerance)
    return jsonify({"status": status, "image": file_path, "name": name, "message": message})


@app.route('/face/validate', methods=['POST'])
def face_validate():
    """
    :param file 需要对比的图片
    :return: {"status": status,"message": message,'data':res,'face_size': 人脸数}
    """
    face = request.files['file']
    if face is None:
        return jsonify({"status": -1, "message": '请求缺少图片文件'})
    json, face_size = face_recognition_manager.validate_img(face)
    if face_size > 0:
        return jsonify({
            'status': '1',
            'face_size': face_size,
            'message': 'success',
            'data': json
        })
    return jsonify({
        'status': '0',
        'face_size': '0',
        'message': 'fail',
        'data': ''
    })