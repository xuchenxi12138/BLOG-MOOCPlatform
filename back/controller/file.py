from flask import Blueprint, request, make_response, send_file, jsonify
from database import MyDatabase
import uuid
from database import MyDatabase
from PIL import Image
rootpath = 'H:/File'

fileModule = Blueprint('file', __name__)


@fileModule.route("/image/<filename>", methods=['GET'])
def get_image(filename):
    dir_name = '/image/'
    file = rootpath + dir_name + filename
    response = make_response(send_file(file))
    response.headers["Content-Disposition"] = "attachment; filename={};".format(file)
    return response


@fileModule.route("/video/<filename>", methods=['GET'])
def get_video(filename):
    dir_name = '/video/'
    file = rootpath + dir_name + filename
    response = make_response(send_file(file))
    response.headers["Content-Disposition"] = "attachment; filename={};".format(file)
    return response


@fileModule.route("/avatar/<filename>", methods=['GET'])
def get_avatar(filename):
    dir_name = '/avatar/'
    file = rootpath + dir_name + filename
    response = make_response(send_file(file))
    response.headers["Content-Disposition"] = "attachment; filename={};".format(file)
    return response


@fileModule.route("/course_file/<filename>", methods=['GET'])
def course_file(filename):
    dir_name = '/course_file/'
    file = rootpath + dir_name + filename
    response = make_response(send_file(file))
    response.headers["Content-Disposition"] = "attachment; filename={};".format(file)
    return response


# 这个功能要根据实际情况编写，这里这么写没啥意义
@fileModule.route("/uploadOneImage", methods=['POST'])
def upload_one_image():
    dir_name = '/image/'
    file = request.files.get('file')
    filename = file.filename
    arr = filename.split('.')
    file_suffix = arr[len(arr) - 1]
    file_new_name = str(uuid.uuid4()) + '.' + file_suffix
    full_path = rootpath + dir_name + file_new_name
    file.save(full_path)
    return jsonify({
        "alt": file_new_name,
        "url": file_new_name,
    })


@fileModule.route("/upload_word", methods=['POST'])
def upload_file():
    dir_name = "/word/"
    file = request.files.get('file')
    filename = file.filename
    arr = filename.split('.')
    file_suffix= arr[len(arr) - 1]
    file_new_name = str(uuid.uuid4()) + '.' + file_suffix
    full_path = rootpath + dir_name + file_new_name
    file.save(full_path)
    return jsonify({
        "alt": file_new_name,
        "url": file_new_name,
    })


def save_file(file,dir_name):
    filename = file.filename
    arr = filename.split('.')
    file_suffix = arr[len(arr) - 1]
    file_new_name = str(uuid.uuid4()) + '.' + file_suffix
    full_path = rootpath + dir_name + file_new_name
    file.save(full_path)
    return jsonify({
        "id": file_new_name,
    })


@fileModule.route("/upload_course_file", methods=['POST'])
def upload_course_file():
    dir_name = "/course_file/"
    file = request.files.get('file')
    res=save_file(file,dir_name)
    return res


@fileModule.route("/upload_video", methods=['POST'])
def upload_video():
    dir_name = "/video/"
    file = request.files.get('file')
    res = save_file(file, dir_name)
    return res


@fileModule.route("/uploadTextImage", methods=['POST'])
def upload_text_image():
    dir_name = '/image/'
    # print(request.files)
    res = {
        "errno": 0,
        "data": []
    }
    for item in request.files:
        file = request.files.get(item)
        filename = file.filename
        arr = filename.split('.')
        file_suffix = arr[len(arr) - 1]
        file_new_name = str(uuid.uuid4()) + '.' + file_suffix
        full_path = rootpath + dir_name + file_new_name
        file.save(full_path)
        res["data"].append({
            "url": "http://localhost:5000/file/image/" + file_new_name,
            "alt": filename,
            "href": ""
        })
    return jsonify(res)


@fileModule.route("/word/<filename>", methods=['GET'])
def get_file(filename):
    dir_name = '/word/'
    file = rootpath + dir_name + filename
    response = make_response(send_file(file))
    response.headers["Content-Disposition"] = "attachment; filename={};".format(file)
    return response


@fileModule.route("/test_upload", methods=["POST"])
def test_upload():
    print(request.form)
    print(request.values)
    print(request.args)
    print(request.files)
    return "OK"


@fileModule.route("/lesson/<lesson_id>", methods=['GET'])
def get_video_by_lesson_id(lesson_id):
    dir_name = '/video/'
    sql=f'select * from lesson_chapter where lesson_id="{lesson_id}" order by chapter_index;'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    res1=cursor.fetchone()
    video_id=""
    if res1:
        sql=f'select * from lesson_subchapter where chapter_id="{res1["chapter_id"]}";'
        cursor.execute(sql)
        res2=cursor.fetchone()
        if res2:
            video_id=res2["video_id"]
    file = rootpath + dir_name + video_id
    response = make_response(send_file(file))
    response.headers["Content-Disposition"] = "attachment; filename={};".format(file)
    connect.close()
    return response


@fileModule.route("/subchapter/<subchapter_id>", methods=['GET'])
def get_video_by_subchapter_id(subchapter_id):
    dir_name = '/video/'
    sql=f'select * from lesson_subchapter where subchapter_id="{subchapter_id}";'
    db=MyDatabase()
    res1=db.query_one(sql,True)
    video_id="empty.mp4"
    if res1 :
        if res1["video_id"]:
            video_id=res1["video_id"]
    file = rootpath + dir_name + video_id
    response = make_response(send_file(file))
    response.headers["Content-Disposition"] = "attachment; filename={};".format(file)
    return response


@fileModule.route("/read_teacher_excel",methods=["POST"])
def read_teacher_excel():
    dir_path="/excel"
    # file=request.files.get("file")
    print(request.files)
    return jsonify([{"username":"xuchenxi"}])


@fileModule.route("/uploadCover",methods=["POST"])
def upload_cover():
    dir_name = '/image/'
    file = request.files.get('file')
    filename = file.filename
    arr = filename.split('.')
    file_suffix = arr[len(arr) - 1]
    file_new_name = str(uuid.uuid4()) + '.' + file_suffix
    full_path = rootpath + dir_name + file_new_name
    file.save(full_path)
    # 裁剪封面
    img = Image.open(full_path)
    width = img.size[0]
    height = img.size[1]
    if width * 0.618 > height:
        target_width = height / 0.618
        start_width = (width - target_width) / 2
        end_width = start_width + target_width
        size = (start_width, 0, end_width, height)
        # print(size)
        new_img = img.crop(size)
        new_img.save(full_path)
    elif width < height / 0.618:
        target_height = width * 0.618
        start_height = (height - target_height) / 2
        end_height = (start_height + target_height)
        size = (0, start_height, width, end_height)
        # print(size)
        new_img = img.crop(size)
        new_img.save(full_path)
    return jsonify({
        "alt": file_new_name,
        "url": file_new_name,
    })