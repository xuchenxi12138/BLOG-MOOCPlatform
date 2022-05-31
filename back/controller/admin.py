import json
import datetime
from flask import Blueprint, url_for, request, render_template, session, redirect, jsonify, json
from database import MyDatabase
from flask_cors import CORS
from controller.file import rootpath
import uuid

# 创建了一个蓝图对象
adminModule = Blueprint('adminModule', __name__)

CORS(adminModule, supports_credentials=True)


@adminModule.route('/', methods=["GET"])
def index():
    return 'this is admin module...'


# 设置首页
@adminModule.route('/get_recommend_list', methods=['GET'])
def get_recommend_list():
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    sql = 'select * from home_recommend_work  order by time limit 0,4'
    cursor.execute(sql)
    response = cursor.fetchall()
    connect.close()
    return jsonify(response)


@adminModule.route('/set_recommend_work', methods=["POST"])
def set_recommend_work():
    form = request.form
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    sql = f'update home_recommend_work ' \
          f'set title="{form["title"]}",type="{form["type"]}",author="{form["author"]}",' \
          f'author_url="{form["author_url"]}",url="{form["url"]}"' \
          f'where id="{form["id"]}";'
    try:
        cursor.execute(sql)
        connect.commit()
        connect.close()
        return jsonify({
            "result": "OK"
        })
    except:
        print(connect.rollback())
        connect.close()
        return jsonify({
            "result": "ERROR"
        })


@adminModule.route('/set_recommend_work_cover', methods=["POST"])
def set_recommend_work_cover():
    dir_name = '/image/'
    # print(request.files)
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    file = request.files.get('file')
    id = request.form.get('id')
    filename = file.filename
    arr = filename.split('.')
    file_suffix = arr[len(arr) - 1]
    file_new_name = str(uuid.uuid4()) + '.' + file_suffix
    full_path = rootpath + dir_name + file_new_name
    file.save(full_path)
    sql = f'update home_recommend_work set cover_url="{file_new_name}"  where id="{id}"'
    try:
        cursor.execute(sql)
        connect.commit()

    except ValueError:
        print(ValueError)
        print(connect.rollback())
    connect.close()
    return jsonify({
        "alt": file_new_name,
        "url": "http://localhost:5000/file/image/" + file_new_name,
    })


# 教师管理模块
@adminModule.route('/get_teacher_list', methods=["GET"])
def get_teacher_list():
    college = request.args.get("college")
    text = request.args.get("text")
    if text:
        pass
    else:
        text = ""
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    start = request.args.get("start")
    end = request.args.get("end")
    sql = "select count(*) from teacher"
    cursor.execute(sql)
    count = cursor.fetchone()
    sql = f'select username,name,college,email from teacher_info where college="{college}" and name like "%{text}%" limit {start},{end} '
    cursor.execute(sql)
    result = cursor.fetchall()
    list = []
    for item in result:
        sql = f'select password from teacher where username="{item["username"]}"'
        cursor.execute(sql)
        res2 = cursor.fetchone();
        item["password"] = res2["password"]
        list.append(item)
    response = {
        "total": count["count(*)"],
        "list": list
    }
    connect.close()
    return jsonify(response)


@adminModule.route('/create_teacher', methods=["POST"])
def create_teacher():
    form = request.form
    response = {
        "result": "",
        "message": ""
    }
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    try:
        username = form.get("username")
        sql = f'select * from teacher where username="{username}";'
        cursor.execute(sql)
        count = cursor.rowcount
        sql = f'select * from student where username="{username}";'
        cursor.execute(sql)
        count = count + cursor.rowcount
        sql = f'select * from admin where username="{username}";'
        cursor.execute(sql)
        count = count + cursor.rowcount
        if count > 0:
            response = {
                "result": "ERROR",
                "message": "这个账号已经存在，不可创建",
                "type": "error"
            }
        else:
            sql1 = f'insert into teacher (username,password) values ("{form["username"]}","{form["password"]}")'
            cursor.execute(sql1)
            sql2 = f'insert into teacher_info (username,name,gender,college,email) ' \
                   f'values ("{form["username"]}","{form["name"]}","{form["gender"]}",' \
                   f'"{form["college"]}","{form["email"]}");'
            print(sql2)
            cursor.execute(sql2)
            connect.commit()
            response = {
                "result": "OK",
                "message": f'上传{form["username"]}成功',
                "type": "success"
            }
    except ValueError:
        print(ValueError)
        print(connect.rollback())
        response = {
            "result": "ERROR",
            "message": connect.rollback(),
            "type": "error"
        }
    connect.close()
    return jsonify(response)


@adminModule.route('edit_teacher', methods=["POST"])
def edit_teacher():
    form = request.form
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    # print(form["username"])
    sql = f'update teacher set password="{form["password"]}" where username="{form["username"]}"'
    sql2 = f'update teacher_info set name="{form["name"]}",gender="{form["gender"]}",' \
           f'college="{form["college"]}",email="{form["email"]}" where username="{form["username"]}"'
    response = {}
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        connect.commit()
        response["message"] = "上传成功"
        response["type"] = "success"
        response["result"] = "OK"
    except ValueError:
        print(ValueError)
        response["message"] = "上传失败，数据库访问失败"
        response["type"] = "error"
        response["result"] = "OK"
    connect.close()
    return jsonify(response)


@adminModule.route('/delete_teacher', methods=["POST"])
def delete_teacher():
    form = request.form
    sql = f'delete from teacher where username="{form["username"]}"'
    sql2 = f'delete from teacher_info where username="{form["username"]}"'
    response = {}
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        connect.commit()
        response["message"] = f'删除{form["username"]}成功'
        response["type"] = "success"
        response["result"] = "OK"
    except ValueError:
        print(ValueError)
        response["message"] = "数据库访问失败"
        response["type"] = "error"
        response["result"] = "OK"
    print(response)
    connect.close()
    return jsonify(response)


# 学生管理模块
@adminModule.route('/get_student_list', methods=["GET"])
def get_student_list():
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    start = request.args.get("start")
    end = request.args.get("end")
    sql = "select count(*) from student"
    cursor.execute(sql)
    count = cursor.fetchone()
    sql = f'select * from student limit {start},{end}'
    cursor.execute(sql)
    result = cursor.fetchall()
    list = []
    for item in result:
        sql = f'select * from student_info where username="{item["username"]}"'
        cursor.execute(sql)
        result_t = cursor.fetchone();
        data = {
            "username": item["username"],
            "password": item["password"],
            "email": result_t["email"],
            "name": result_t["name"],
            "gender": result_t["gender"],
            "college": result_t["college"]
        }
        list.append(data)
    response = {
        "total": count["count(*)"],
        "list": list
    }
    connect.close()
    return jsonify(response)


@adminModule.route('/create_student', methods=["POST"])
def create_student():
    form = request.form
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    response = {
        "result": "",
        "message": ""
    }
    try:
        username = form.get("username")
        sql = f'select * from teacher where username="{username}";'
        cursor.execute(sql)
        count = cursor.rowcount
        sql = f'select * from student where username="{username}";'
        cursor.execute(sql)
        count = count + cursor.rowcount
        sql = f'select * from admin where username="{username}";'
        cursor.execute(sql)
        count = count + cursor.rowcount
        if count > 0:
            response = {
                "result": "ERROR",
                "message": "这个账号已经存在，不可创建",
                "type": "error"
            }
        else:
            sql1 = f'insert into student (username,password) values ("{form["username"]}","{form["password"]}")'
            cursor.execute(sql1)
            sql2 = f'insert into student_info (username,name,gender,college,email) ' \
                   f'values ("{form["username"]}","{form["name"]}","{form["gender"]}",' \
                   f'"{form["college"]}","{form["email"]}");'
            print(sql2)
            cursor.execute(sql2)
            connect.commit()
            response = {
                "result": "OK",
                "message": f'上传{form["username"]}成功',
                "type": "success"
            }
    except ValueError:
        print(ValueError)
        print(connect.rollback())
        response = {
            "result": "ERROR",
            "message": connect.rollback(),
            "type": "error"
        }
    connect.close()
    return jsonify(response)


@adminModule.route('edit_student', methods=["POST"])
def edit_student():
    form = request.form
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    sql = f'update student set password="{form["password"]}" where username="{form["username"]}"'
    sql2 = f'update student_info set name="{form["name"]}",gender="{form["gender"]}",' \
           f'college="{form["college"]}",email="{form["email"]}" where username="{form["username"]}"'
    response = {}
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        connect.commit()
        response["message"] = "上传成功"
        response["type"] = "success"
        response["result"] = "OK"
    except ValueError:
        print(ValueError)
        response["message"] = "上传失败，数据库访问失败"
        response["type"] = "error"
        response["result"] = "OK"
    connect.close()
    return jsonify(response)


@adminModule.route('/delete_student', methods=["POST"])
def delete_student():
    form = request.form
    sql = f'delete from student where username="{form["username"]}"'
    sql2 = f'delete from student_info where username="{form["username"]}"'
    response = {}
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        connect.commit()
        response["message"] = f'删除{form["username"]}成功'
        response["type"] = "success"
        response["result"] = "OK"
    except ValueError:
        print(ValueError)
        response["message"] = "数据库访问失败"
        response["type"] = "error"
        response["result"] = "OK"
    print(response)
    connect.close()
    return jsonify(response)


@adminModule.route('/get_teacher_name', methods=["GET"])
def get_teacher_name():
    id = request.args.get("id")
    sql = f'select name from teacher_info where username="{id}"'
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    cursor.execute(sql)
    result = cursor.fetchone()
    connect.close()
    if result:
        return jsonify({
            "name": result["name"],
            "type": "success"
        })
    else:
        return jsonify({
            "message": "找不到该教师",
            "type": "error"
        })


@adminModule.route('/get_lesson_name', methods=["GET"])
def get_lesson_name():
    id = request.args.get("id")
    sql = f'select lesson_name from lesson where lesson_id="{id}"'
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    cursor.execute(sql)
    result = cursor.fetchone()
    connect.close()
    if result:
        return jsonify({
            "lesson_name": result["lesson_name"],
            "type": "success"
        })
    else:
        return jsonify({
            "message": "找不到该课程",
            "type": "error"
        })


# 班级管理模块
@adminModule.route('/get_class_list', methods=["GET"])
def get_class_list():
    start = request.args.get("start")
    end = request.args.get("end")
    sql = "select count(*) from class"
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    cursor.execute(sql)
    count = cursor.fetchone()
    sql = f'select * from class limit {start},{end}'
    cursor.execute(sql)
    result = cursor.fetchall()
    for item in result:
        sql1 = f'select name from teacher_info where username="{item["teacher_id"]}"'
        cursor.execute(sql1)
        res1 = cursor.fetchone()
        if res1:
            item["teacher_name"] = res1["name"]
        sql1 = f'select lesson_name from lesson where lesson_id="{item["lesson_id"]}"'
        cursor.execute(sql1)
        res2 = cursor.fetchone()
        if res2:
            item["lesson_name"] = res2["lesson_name"]
    response = {
        "total": count["count(*)"],
        "list": result
    }
    connect.close()
    return jsonify(response)


@adminModule.route('/create_class', methods=["POST"])
def create_class():
    form = request.form
    print(form)
    response = {
        "result": "",
        "message": ""
    }
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    try:
        class_id = form.get("class_id")
        teacher_id = form.get("teacher_id")
        sql = f'select * from class where class_id="{class_id}";'
        cursor.execute(sql)
        if cursor.rowcount > 0:
            response = {
                "result": "ERROR",
                "message": "这个课程号已经存在，不可创建"
            }
        else:
            sql = f'insert into class (class_id,class_name,college,teacher_id,lesson_id) values ' \
                  f'("{form["class_id"]}","{form["class_name"]}","{form["college"]}",' \
                  f'"{form["teacher_id"]}","{form["lesson_id"]}");'
            cursor.execute(sql)
            connect.commit()
            response = {
                "result": "OK",
                "message": f'上传{form["class_id"]}成功',
                "type": "success"
            }
    except ValueError:
        print(ValueError)
        print(connect.rollback())
        response = {
            "result": "ERROR",
            "message": connect.rollback(),
        }
    connect.close()
    return jsonify(response)


@adminModule.route('/edit_class', methods=["POST"])
def edit_class():
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    form = request.form
    response = {}
    sql = f'select count(*) from class where class_id="{form["class_id"]}"'
    cursor.execute(sql)
    result = cursor.fetchone()
    # if form["lesson_id"]:

    if result["count(*)"] == 0 and form["class_id"] != "null" and form["class_id"] != "":
        response = {
            "result": "ERROR",
            "message": '课程码不存在',
            "type": "error"
        }
    else:
        sql2 = f'update class set class_name="{form["class_name"]}",college="{form["college"]}",' \
               f'teacher_id="{form["teacher_id"]}",' \
               f'lesson_id="{form["lesson_id"]}" ' \
               f'where class_id="{form["class_id"]}";'
        cursor.execute(sql2)
        connect.commit()
        response = {
            "result": "OK",
            "message": f'修改{form["class_id"]}成功',
            "type": "success"
        }
    connect.close()
    return jsonify(response)


@adminModule.route('/delete_class', methods=["POST"])
def delete_class():
    form = request.form
    sql = f'delete from class where class_id="{form["class_id"]}"'
    print(sql)
    response = {}
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    try:
        cursor.execute(sql)
        connect.commit()
        response["message"] = f'删除班级{form["class_id"]}成功'
        response["type"] = "success"
        response["result"] = "OK"
    except ValueError:
        print(ValueError)
        response["message"] = "删除成功，数据库访问失败"
        response["type"] = "error"
        response["result"] = "OK"
    connect.close()
    return jsonify(response)


# 课程管理模块
@adminModule.route('/get_lesson_list', methods=["GET"])
def get_lesson_list():
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    start = request.args.get("start")
    end = request.args.get("end")
    sql = "select count(*) from lesson"
    cursor.execute(sql)
    count = cursor.fetchone()
    sql = f'select * from lesson limit {start},{end}'
    cursor.execute(sql)
    result = cursor.fetchall()
    for item in result:
        sql1 = f'select name from teacher_info where username="{item["teacher_id"]}"'
        cursor.execute(sql1)
        res1 = cursor.fetchone()
        if res1:
            item["teacher_name"] = res1["name"]
    response = {
        "total": count["count(*)"],
        "list": result
    }
    connect.close()
    return jsonify(response)


@adminModule.route('/create_lesson', methods=["POST"])
def create_lesson():
    form = request.form
    print(form)
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    response = {
        "result": "",
        "message": ""
    }
    try:
        lesson_id = form.get("lesson_id")
        teacher_id = form.get("teacher_id")
        sql = f'select * from lesson where lesson_id="{lesson_id}";'
        cursor.execute(sql)
        if cursor.rowcount > 0:
            response = {
                "result": "ERROR",
                "message": "这个课程号已经存在，不可创建"
            }
        else:
            sql = f'insert into lesson (lesson_id,lesson_name,college,teacher_id) values ' \
                  f'("{form["lesson_id"]}","{form["lesson_name"]}","{form["college"]}",' \
                  f'"{form["teacher_id"]}");'
            cursor.execute(sql)
            connect.commit()
            response = {
                "result": "OK",
                "message": f'上传{form["lesson_id"]}成功',
                "type": "success"
            }
    except ValueError:
        print(ValueError)
        print(connect.rollback())
        response = {
            "result": "ERROR",
            "message": connect.rollback(),
        }
    connect.close()
    return jsonify(response)


@adminModule.route('/edit_lesson', methods=["POST"])
def edit_lesson():
    form = request.form
    response = {}
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    sql = f'select count(*) from lesson where lesson_id="{form["lesson_id"]}"'
    cursor.execute(sql)
    result = cursor.fetchone()
    # if form["lesson_id"]:

    if result["count(*)"] == 0 and form["lesson_id"] != "null" and form["lesson_id"] != "":
        response = {
            "result": "ERROR",
            "message": '课程码不存在',
            "type": "error"
        }
    else:
        sql2 = f'update lesson set lesson_name="{form["lesson_name"]}",college="{form["college"]}",' \
               f'teacher_id="{form["teacher_id"]}" ' \
               f'where lesson_id="{form["lesson_id"]}";'
        cursor.execute(sql2)
        connect.commit()
        response = {
            "result": "OK",
            "message": f'修改{form["lesson_id"]}成功',
            "type": "success"
        }
    connect.close()
    return jsonify(response)


@adminModule.route('/delete_lesson', methods=["POST"])
def delete_lesson():
    form = request.form
    sql = f'delete from lesson where lesson_id="{form["lesson_id"]}"'
    print(sql)
    response = {}
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    try:
        cursor.execute(sql)
        connect.commit()
        response["message"] = f'删除班级{form["lesson_id"]}成功'
        response["type"] = "success"
        response["result"] = "OK"
    except ValueError:
        print(ValueError)
        response["message"] = "删除成功，数据库访问失败"
        response["type"] = "error"
        response["result"] = "OK"
    connect.close()
    return jsonify(response)


# 管理员模块
@adminModule.route('/get_admin_list', methods=["GET"])
def get_admin_list():
    start = request.args.get("start")
    end = request.args.get("end")
    sql = "select count(*) from admin"
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    cursor.execute(sql)
    count = cursor.fetchone()
    sql = f'select * from admin limit {start},{end}'
    cursor.execute(sql)
    result = cursor.fetchall()
    list = []
    for item in result:
        sql = f'select * from admin_info where username="{item["username"]}"'
        cursor.execute(sql)
        result_t = cursor.fetchone();
        data = {
            "username": item["username"],
            "password": item["password"],
            "email": result_t["email"],
            "name": result_t["name"],
            "gender": result_t["gender"],
            "college": result_t["college"]
        }
        list.append(data)
    response = {
        "total": count["count(*)"],
        "list": list
    }
    connect.close()
    return jsonify(response)


@adminModule.route('/create_admin', methods=["POST"])
def create_admin():
    form = request.form
    response = {
        "result": "",
        "message": ""
    }
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    try:
        username = form.get("username")
        sql = f'select * from teacher where username="{username}";'
        cursor.execute(sql)
        count = cursor.rowcount
        sql = f'select * from student where username="{username}";'
        cursor.execute(sql)
        count = count + cursor.rowcount
        sql = f'select * from admin where username="{username}";'
        cursor.execute(sql)
        count = count + cursor.rowcount
        if count > 0:
            response = {
                "result": "ERROR",
                "message": "这个账号已经存在，不可创建",
                "type": "error"
            }
        else:
            sql1 = f'insert into admin (username,password) values ("{form["username"]}","{form["password"]}")'
            cursor.execute(sql1)
            sql2 = f'insert into admin_info (username,name,gender,college,email) ' \
                   f'values ("{form["username"]}","{form["name"]}","{form["gender"]}",' \
                   f'"{form["college"]}","{form["email"]}");'
            print(sql2)
            cursor.execute(sql2)
            connect.commit()
            response = {
                "result": "OK",
                "message": f'上传{form["username"]}成功',
                "type": "success"
            }
    except ValueError:
        print(ValueError)
        print(connect.rollback())
        response = {
            "result": "ERROR",
            "message": connect.rollback(),
            "type": "error"
        }
    connect.close()
    return jsonify(response)


@adminModule.route('edit_admin', methods=["POST"])
def edit_admin():
    form = request.form

    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    sql = f'update admin set password="{form["password"]}" where username="{form["username"]}"'
    sql2 = f'update admin_info set name="{form["name"]}",gender="{form["gender"]}",' \
           f'college="{form["college"]}",email="{form["email"]}" where username="{form["username"]}"'
    response = {}
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        connect.commit()
        response["message"] = "上传成功"
        response["type"] = "success"
        response["result"] = "OK"
    except ValueError:
        print(ValueError)
        response["message"] = "上传失败，数据库访问失败"
        response["type"] = "error"
        response["result"] = "OK"
    connect.close()
    return jsonify(response)


@adminModule.route('/delete_admin', methods=["POST"])
def delete_admin():
    form = request.form
    sql = f'delete from admin where username="{form["username"]}"'
    sql2 = f'delete from admin_info where username="{form["username"]}"'
    response = {}
    db = MyDatabase()
    cursor = db.cursor
    connect = db.connect
    try:
        cursor.execute(sql)
        cursor.execute(sql2)
        connect.commit()
        response["message"] = f'删除{form["username"]}成功'
        response["type"] = "success"
        response["result"] = "OK"
    except ValueError:
        print(ValueError)
        response["message"] = "数据库访问失败"
        response["type"] = "error"
        response["result"] = "OK"
    print(response)
    connect.close()
    return jsonify(response)


@adminModule.route('/search_teacher', methods=["GET"])
def search_teacher():
    text = request.args.get("text")
    college = request.args.get("college")
    sql = f'select * from teacher_info where name like "%{text}%" and college="{college}"'
    db = MyDatabase()
    res = db.query(sql)
    for item in res:
        if item:
            sql = f'select password from teacher where username="{item["username"]}";'
            res2 = db.query_one(sql)
            item["password"] = res2["password"]
    db.connect.close()
    return jsonify(res)


@adminModule.route("/upload_teacher_table", methods=["POST"])
def upload_teacher_table():
    data = json.loads(request.form.get("data"))
    response=[]
    for item in data:
        db = MyDatabase()
        sql=f'select * from teacher where username="{item["username"]}";'
        res=db.query_one(sql)
        if res:
            item["type"] = "warning"
            item["message"]="该工号已经存在"
            response.append(item)
        else:
            sql1 = f'insert into teacher (username,password) values ("{item["username"]}","{item["password"]}");'
            sql2 = f'insert into teacher_info (username,name,gender,college,email) values ' \
                   f'("{item["username"]}","{item["name"]}","{item["gender"]}","{item["college"]}","{item["email"]}");'
            db.curd(sql1)
            db.curd(sql2)
            item["type"] = "success"
            item["message"] = "添加成功"
            response.append(item)
    db.connect.close()
    return jsonify(response)
