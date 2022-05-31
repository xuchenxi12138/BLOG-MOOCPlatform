from ast import Not
import time
from urllib import response
import uuid

from flask import Blueprint, url_for, request, render_template, session, redirect, jsonify
# from database import cursor
from database import MyDatabase

studentModule = Blueprint('studentModule', __name__)


@studentModule.route("/", methods=["GET"])
def index():
    return "这是学生模块..."


@studentModule.route("/get_info", methods=["GET"])
def get_info():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    username = request.args.get("username")
    sql = f'select nickname,name,signature,avatar from student_info where username="{username}"'
    cursor.execute(sql)
    result = cursor.fetchone()
    connect.close()
    return jsonify(result)


@studentModule.route("/change_signature", methods=["POST"])
def change_signature():
    username = request.form.get("username")
    signature = request.form.get("signature")
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    sql = f'update student_info set signature="{signature}" where username="{username}"'
    cursor.execute(sql)
    connect.commit()
    result = cursor.fetchone()
    connect.close()
    return jsonify(result)


@studentModule.route("/get_class_list", methods=["GET"])
def get_class_list():
    username = request.args.get("username")
    sql = f'select * from student_list where student_id="{username}"'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    result = cursor.fetchall()
    data = []
    for item in result:
        sql = f'select * from class where class_id="{item["class_id"]}"'
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
            sql = f'select lesson_name from lesson where lesson_id="{res["lesson_id"]}"'
            cursor.execute(sql)
            res2 = cursor.fetchone()
            if res2:
                res["lesson_name"] = res2["lesson_name"]
        sql = f'select count(*) from assignment_a where student_id="{username}" and finished="0" ' \
              f'and class_id="{item["class_id"]}";'
        cursor.execute(sql)
        res3 = cursor.fetchone()
        res["messageNumber"] = res3["count(*)"]
        data.append(res)
    connect.close()
    return jsonify(data)


@studentModule.route("/get_all_assignments", methods=["GET"])
def get_all_assignments():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    username = request.args.get("username")
    class_id = request.args.get("class_id")
    # 查找所有属于这个班级和学生之间的作业，然后查找是否都创建了记录，如果有记录不完整的就插入。
    # 这个设计io量太大了，属实鸡肋
    sql=f'select * from assignment_q where class_id="{class_id}"'
    cursor.execute(sql)
    res=cursor.fetchall()
    for item in res:
        sql=f'select * from assignment_a where assignment_id="{item["id"]}" and student_id="{username}"'
        cursor.execute(sql)
        res2=cursor.fetchone()
        if res2:
            pass
        else:
            sql=f'insert into assignment_a (student_id,assignment_id,class_id,score,finished,post_time)'\
                f'values ("{username}","{item["id"]}","{class_id}",0,0,"{item["post_time"]}");'
            cursor.execute(sql)
            connect.commit()
    sql = f'select * from assignment_a where student_id="{username}" and class_id="{class_id}"'
    cursor.execute(sql)
    res = cursor.fetchall()
    for item in res:
        sql = f'select post_time,title,file_id,description,deadline from assignment_q' \
              f' where id="{item["assignment_id"]}"'
        cursor.execute(sql)
        res2 = cursor.fetchone()
        item["post_time"] = str(res2["post_time"])
        item["title"] = res2["title"]
        item["q_file_id"] = res2["file_id"]
        item["description"] = res2["description"]
        item["deadline"] = str(res2["deadline"])
    connect.close()
    return jsonify(res)


@studentModule.route("/hand_on_assignment", methods=["POST"])
def hand_on_assignment():
    username = request.form.get("username")
    file_id = request.form.get("file_id")
    assignment_id = request.form.get("assignment_id")
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    sql = f'update assignment_a set file_id="{file_id}",finished="1",post_time=now() ' \
          f'where student_id="{username}" and assignment_id="{assignment_id}"'
    response = {
        "message": "访问数据库失败",
        "type": 'error'
    }
    try:
        cursor.execute(sql)
        connect.commit()
        response = {
            "message": "上传成功",
            "type": 'success'
        }
    except ValueError:
        print(ValueError)
    connect.close()
    return jsonify(response)


@studentModule.route("/get_blogs", methods=['GET'])
def get_blogs():
    username = request.args.get("username")
    start = request.args.get("start")
    end = int(start) + 10
    sql = f'select * from blog where blog_owner_id="{username}" and identification="student" ' \
          f'order by post_time desc limit {start},{end} '
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    result = cursor.fetchall()
    total = cursor.rowcount
    if result:
        for item in result:
            sql = f'select name,nickname,avatar from student_info where username="{item["blog_owner_id"]}"'
            cursor.execute(sql)
            res1 = cursor.fetchone()
            item["blog_owner_name"] = res1["name"]
            item["nickname"] = res1["nickname"]
            item["avatar"] = res1["avatar"]
            item["identification"] = "student"
            item["post_time"] = str(item["post_time"])
            sql = f'select state from like_table where username="{username}" and work_id="{item["blog_id"]}" ' \
                  f'and identification="student";'
            cursor.execute(sql)
            res2 = cursor.fetchone()
            if res2:
                item["liked"] = res2["state"]
            else:
                item["liked"] = False
        response = {
            "list": result,
            "total": total
        }
    else:
        response = {
            "message": "nomore",
            "type": "error"
        }
    connect.close()
    return jsonify(response)


@studentModule.route("/get_my_info", methods=["GET"])
def get_my_info():
    username = request.args.get("username")
    sql = f'select * from student_info where username="{username}"'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    result = cursor.fetchone()
    response = {
        "username": username,
        "name": result["name"],
        "college": result["college"],
        "nickname": result["nickname"],
        "phone_number": result["phone_number"],
        "email": result["email"],
        "degree": result["degree"],
        "entrance_date": result["entrance_date"],
        "birthday": result["birthday"],
        "major": result["major"],
        "gender": result["gender"],
        "avatar": result["avatar"],
    }
    connect.close()
    return jsonify(response)


@studentModule.route("/edit_my_info", methods=["POST"])
def edit_my_info():
    form = request.form
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    print(form)
    response = {}
    sql = f'update student_info set name="{form["name"]}",' \
          f'gender="{form["gender"]}",nickname="{form["nickname"]}",' \
          f'phone_number="{form["phone_number"]}",email="{form["email"]}",' \
          f'college="{form["college"]}",major="{form["major"]}",' \
          f'degree="{form["degree"]}",entrance_date="{form["entrance_date"]}",birthday="{form["birthday"]}",' \
          f'avatar="{form["avatar"]}"' \
          f' where username="{form["username"]}";'

    try:
        cursor.execute(sql)
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


@studentModule.route("/change_password", methods=['POST'])
def change_password():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    username = request.form.get("username")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    sql = f'select password from student where username="{username}"'
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    response = {}
    if result["password"] == old_password:
        try:
            sql = f'update student set password="{new_password}" where username="{username}"'
            cursor.execute(sql)
            connect.commit()
            response = {
                "message": "修改密码成功",
                "type": "success"
            }
        except ValueError:
            print(ValueError)
            response = {
                "message": "访问数据库失败",
                "type": "error"
            }
    else:
        response = {
            "message": "密码不正确",
            "type": "error"
        }
    connect.close()
    return jsonify(response)


@studentModule.route("/get_class_by_id", methods=["GET"])
def get_class_by_id():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    class_id = request.args.get("class_id")
    sql = f'select * from class where class_id="{class_id}"'
    cursor.execute(sql)
    res = cursor.fetchone()
    if res:
        response = {
            "message": {
                "message": "OK",
                "type": "success"
            },
            "class_info": {
                "class_id": class_id,
                "class_name": res["class_name"],
                "college": res["college"]
            }
        }
    else:
        response = {"message": {"message": "找不到班级", "type": "error"}}
    connect.close()
    return jsonify(response)


@studentModule.route("/get_class_by_name", methods=["GET"])
def get_class_by_name():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    class_name = request.args.get("class_name")
    sql = f'select * from class where class_name like "%{class_name}%"'
    cursor.execute(sql)
    res = cursor.fetchall()
    response={}
    message=""
    
    if res:
        for item in res:
            if item["teacher_id"]:
                sql = f'select name from teacher_info where username="{item["teacher_id"]}"'
                cursor.execute(sql)
                res1 = cursor.fetchone()
                item["teacher_name"] = res1['name']
                message = message + "<br><br>班级码：" + item["class_id"] + "<br>名称：" \
                          + item["class_name"] + "<br>教师：" + item["teacher_name"] + "<br>学院：" + item["college"]
        print(res)
        response = {
            "message": {
                "message": "OK",
                "type": "success"
            },
            "class_info":message
        }
    else:
        response = {"message": {"message": "找不到班级", "type": "error"}}
    connect.close()
    return jsonify(response)


@studentModule.route("/search_class",methods=["GET"])
def search_class():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    text=request.args.get("text")
    sql1=f'select * from class where class_name like "%{text}%" or class_id like "%{text}%"'
    cursor.execute(sql1)
    res1=cursor.fetchall()
    sql2=f'select * from teacher_info where name like "%{text}%";'
    cursor.execute(sql2)
    res2=cursor.fetchall()
    if res2:
        for item in res2:
            sql3=f'select * from class where teacher_id="{item["teacher_id"]}"'
            cursor.execute(sql3)
            res3=cursor.fetchall()
            for subitem in res3:
                if subitem not in res1:
                    res1.append(subitem)
    connect.close()
    return jsonify(res1)


@studentModule.route("/join_class",methods=["GET"])
def join_class():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    username=request.args.get("username")
    class_id=request.args.get("class_id")
    sql1=f'select * from student_list where class_id="{class_id}" and student_id="{username}";'
    cursor.execute(sql1)
    res1=cursor.fetchone()
    res={}
    if res1:
      res={"message":"已经加入，无需添加","type":"warning"}
    else: 
        sql2=f'insert into student_list (student_id,class_id) values ("{username}","{class_id}")'
        cursor.execute(sql2)
        connect.commit()
        res={"message":"添加成功","type":"success"}
    connect.close()
    return jsonify(res)