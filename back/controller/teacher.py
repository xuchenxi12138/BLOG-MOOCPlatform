from flask import Blueprint, url_for, request, render_template, session, redirect, jsonify
# from database import cursor
from database import MyDatabase
import uuid
from pymysql.converters import escape_string
teacherModule = Blueprint('teacherModule', __name__)


# from flask_cors import CORS
# CORS(teacherModule, supports_credentials=True)


@teacherModule.route('/', methods=["GET"])
def index():
    return 'start teacher module'


@teacherModule.route("/get_my_info", methods=["GET"])
def get_my_info():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    username = request.args.get("username")
    sql = f'select * from teacher_info where username="{username}"'
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


@teacherModule.route('/get_lesson_name', methods=["GET"])
def get_lesson_name():
    id = request.args.get("lesson_id")
    sql = f'select lesson_name from lesson where lesson_id="{id}"'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
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


@teacherModule.route("/edit_my_info", methods=["POST"])
def edit_my_info():
    form = request.form
    # print(form["username"])
    print(form)
    response = {}
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    sql = f'update teacher_info set name="{form["name"]}",' \
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


@teacherModule.route("/change_password", methods=['POST'])
def change_password():
    print(request.form)
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    username = request.form.get("username")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    sql = f'select password from teacher where username="{username}"'
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    response = {}
    if result["password"] == old_password:
        try:
            sql = f'update teacher set password="{new_password}" where username="{username}"'
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


@teacherModule.route("/get_blogs", methods=['GET'])
def get_blogs():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    username = request.args.get("username")
    start = request.args.get("start")
    end = int(start) + 5
    sql = f'select * from blog where blog_owner_id="{username}" and identification="teacher" ' \
          f'order by post_time desc limit {start},{end} '
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        for item in result:
            sql = f'select name,nickname from teacher_info where username="{item["blog_owner_id"]}"'
            cursor.execute(sql)
            res1 = cursor.fetchone()
            item["blog_owner_name"] = res1["name"]
            item["nickname"] = res1["nickname"]
            item["identification"] = "teacher"
            item["post_time"] = str(item["post_time"])
            sql = f'select state from like_table where username="{username}" and work_id="{item["blog_id"]}" ' \
                  f'and identification="teacher";'
            cursor.execute(sql)
            res2 = cursor.fetchone()
            if res2:
                item["liked"] = res2["state"]
            else:
                item["liked"] = False
    else:
        result = {
            "message": "nomore",
            "type": "error"
        }
    connect.close()
    return jsonify(result)


@teacherModule.route("/get_classes", methods=["GET"])
def get_classes():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    username = request.args.get("username")
    sql = f'select * from class where teacher_id="{username}"'
    cursor.execute(sql)
    result = cursor.fetchall()
    for item in result:
        sql = f'select lesson_name from lesson where lesson_id="{item["lesson_id"]}"'
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
            item["lesson_name"] = res["lesson_name"]
        sql = f'select count(*) from assignment_a where class_id="{item["class_id"]}" and finished="1" ' \
              f'and score="-1";'
        cursor.execute(sql)
        res = cursor.fetchone()
        item["messageNumber"] = res["count(*)"]
    connect.close()
    return jsonify(result)


@teacherModule.route("/edit_class", methods=["POST"])
def edit_class():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    class_id = request.form.get("class_id")
    class_name = request.form.get("class_name")
    lesson_id = request.form.get("lesson_id")
    response = {}
    if lesson_id:
        sql = f'select * from lesson where lesson_id="{lesson_id}"'
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
        if result:
            response = edit(class_id=class_id, class_name=class_name, lesson_id=lesson_id)

        else:
            response = {
                "message": "找不到课程",
                "type": "error"
            }
    else:
        response = edit(class_id=class_id, class_name=class_name, lesson_id="")
    connect.close()
    return jsonify(response)


def edit(class_id, class_name, lesson_id):
    sql = f'update class set class_name="{class_name}",lesson_id="{lesson_id}" where class_id="{class_id}"'
    response = {}
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    try:
        cursor.execute(sql)
        connect.commit()
        response = {
            "message": "修改成功",
            "type": "success"
        }
    except ValueError:
        print(ValueError)
        response = {
            "message": "访问数据库失败",
            "type": "error"
        }
    connect.close()
    return response


@teacherModule.route("/get_student_by_id", methods=["GET"])
def get_student_by_id():
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    username = request.args.get("username")
    sql = f'select name,college,email from student_info where username="{username}"'
    cursor.execute(sql)
    result = cursor.fetchone()
    connect.close()
    if result:
        return jsonify({
            "type": "success",
            "data": result,
            "message": "找到了！！！"
        })
    else:
        return jsonify({
            "type": "error",
            "data": "",
            "message": "没有这个学生！！！"
        })


@teacherModule.route("/get_student_by_name", methods=["GET"])
def get_student_by_name():
    name = request.args.get("name")
    sql = f'select username,name,college,email from student_info where name="{name}"'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    result = cursor.fetchall()
    connect.close()
    if result:
        return jsonify({
            "type": "success",
            "data": result,
            "message": "找到了！！！"
        })
    else:
        return jsonify({
            "type": "error",
            "data": "",
            "message": "没有这个学生！！！"
        })


@teacherModule.route("/add_student", methods=["POST"])
def add_student():
    class_id = request.form.get("class_id")
    username = request.form.get("username")
    sql = f'select * from student_list where class_id="{class_id}" and student_id="{username}";'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    result = cursor.fetchone()
    response = {}
    if result:
        response = {
            "message": "该学生已经存在无需添加",
            "type": "warning"
        }
    else:
        sql = f'select * from student where username="{username}"'
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
            try:
                sql = f'insert into student_list (class_id,student_id) values ' \
                      f'("{class_id}","{username}");'
                cursor.execute(sql)
                connect.commit()
                response = {
                    "message": "添加成功",
                    "type": "success"
                }
            except ValueError:
                print(ValueError)
                response = {
                    "message": "访问数据库失败",
                    "type": "warning"
                }
        else:
            response = {
                "message": "不存在这个学生",
                "type": "warning"
            }
    connect.close()
    return jsonify(response)


@teacherModule.route("/get_students", methods=["GET"])
def get_students():
    class_id = request.args.get("class_id")
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    sql=f'select class_name from class where class_id="{class_id}"'
    cursor.execute(sql)
    result=cursor.fetchone()
    class_name=result["class_name"]
    sql = f'select * from student_list where class_id="{class_id}"'
    cursor.execute(sql)
    result = cursor.fetchall()
    data = []
    for item in result:
        sql = f'select name,username,college,email,gender from student_info where username="{item["student_id"]}"'
        cursor.execute(sql)
        res = cursor.fetchone()
        data.append(res)
    connect.close()
    return jsonify({"student_list":data,"class_name":class_name})


@teacherModule.route("/delete_student", methods=["GET"])
def delete_students():
    class_id = request.args.get("class_id")
    username = request.args.get("username")
    sql = f'delete from student_list where class_id="{class_id}" and student_id="{username}";'
    response = {}
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    try:
        cursor.execute(sql)
        connect.commit()
        response = {
            "message": "删除成功",
            "type": "success"
        }
    except ValueError:
        print(ValueError)
        response = {
            "message": "删除失败",
            "type": "error"
        }
    connect.close()
    return jsonify(response)


@teacherModule.route("/create_assignment", methods=["POST"])
def create_assignment():
    class_id = request.form.get("class_id")
    title = request.form.get("title")
    des = request.form.get("description")
    file_id = request.form.get("file_id")
    teacher_id = request.form.get("teacher_id")
    deadline = request.form.get("deadline")
    assign_id = str(uuid.uuid4())
    response = {}
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    sql = f'insert into assignment_q (id,class_id,teacher_id,title,description,file_id,deadline,post_time)' \
          f'values("{assign_id}","{class_id}","{teacher_id}","{title}","{des}","{file_id}","{deadline}",now())'
    try:
        cursor.execute(sql)
        connect.commit()
        response = {
            "message": "上传成功",
            "type": "success"
        }
        sql = f'select * from student_list where class_id="{class_id}"'
        cursor.execute(sql)
        result = cursor.fetchall()
        # 创建作业记录
        for item in result:
            sql = f'insert into assignment_a (student_id,assignment_id,class_id) ' \
                  f'values("{item["student_id"]}","{assign_id}","{class_id}");'
            cursor.execute(sql)
            connect.commit()
    except ValueError:
        response = {
            "message": "上传失败",
            "type": "error"
        }
    connect.close()
    return jsonify(response)


@teacherModule.route("/get_assignments", methods=["GET"])
def get_assignments():
    class_id = request.args.get("class_id")
    sql = f'select * from assignment_q where class_id="{class_id}" order by post_time;'
    db=MyDatabase()
    result = db.query(sql,True)
    for item in result:
        item["post_time"] = str(item["post_time"])
        item["deadline"] = str(item["deadline"])
    return jsonify(result)


@teacherModule.route("/edit_assignment", methods=["POST"])
def edit_assignment():
    id = request.form.get("id")
    title = request.form.get("title")
    des = request.form.get("description")
    file_id = request.form.get("file_id")
    deadline = request.form.get("deadline")
    response = {}
    sql = f'update assignment_q set title="{title}",description="{des}",file_id="{file_id}",' \
          f'deadline="{deadline}" where id="{id}";'
    try:
        db=MyDatabase()
        db.curd(sql,)
        response = {
            "message": "上传成功",
            "type": "success"
        }
    except ValueError:
        response = {
            "message": "上传失败",
            "type": "error"
        }
    return jsonify(response)


@teacherModule.route('/delete_assignment', methods=["POST"])
def delete_assignment():
    id = request.form.get("id")
    sql = f'delete from assignment_q where id="{id}"'
    db=MyDatabase()

    db.curd(sql)
    sql = f'delete from assignment_a  where assignment_id="{id}"'
    db.curd(sql,True)
    return jsonify({
        "message": "删除成功",
        "type": "success"
    })


@teacherModule.route('/count_assignment', methods=["GET"])
def count_assignment():
    class_id = request.args.get("class_id")
    sql = f'select count(*) from assignment_a where class_id="{class_id}" ' \
          f'and finished="1" and score="0";'
    db=MyDatabase()
    res = db.query_one(sql,True)
    return jsonify({
        "number": res["count(*)"]
    })


@teacherModule.route('/get_new_hand_on', methods=["GET"])
def get_new_hand_on():
    class_id = request.args.get("class_id")
    sql = f'select * from assignment_a where class_id="{class_id}" ' \
          f'and finished="1" and score=0;'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    res = cursor.fetchall()
    for item in res:
        sql = f'select name,username from student_info where username="{item["student_id"]}"'
        cursor.execute(sql)
        res2 = cursor.fetchone()
        item["name"] = res2["name"]
        sql = f'select title,post_time from assignment_q where id="{item["assignment_id"]}"'
        cursor.execute(sql)
        res2 = cursor.fetchone()
        item["title"] = res2["title"]
        item["post_time"] = str(res2["post_time"])
        item["hand_on_time"] = str(item["hand_on_time"])
    connect.close()
    return jsonify(res)


@teacherModule.route('/check_assignment', methods=["POST"])
def check_assignment():
    assignment_id = request.form.get("assignment_id")
    student_id = request.form.get("student_id")
    score = request.form.get("score")
    comment = request.form.get("comment")
    response = {}
    try:
        sql = f'update assignment_a set score="{score}",comment="{comment}" ' \
              f'where assignment_id="{assignment_id}" and student_id="{student_id}"'
        print(sql)
        db=MyDatabase()
        db.curd(sql,True)
        response = {
            "message": "打分上传成功",
            "type": "success"
        }
    except ValueError:
        response = {
            "message": "访问数据库失败",
            "type": "error"
        }
    return jsonify(response)


@teacherModule.route("/get_lesson_list", methods=["GET"])
def get_lesson_list():
    username = request.args.get("username")
    start = request.args.get("start")
    end = int(start) + 10
    sql = f'select * from lesson where teacher_id="{username}" ' \
          f'order by create_time desc limit {start},{end} '
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    result = cursor.fetchall()
    total = cursor.rowcount
    connect.close()
    return jsonify({
        "list": result,
        "total": total
    })


@teacherModule.route("/get_lesson_info", methods=["GET"])
def get_lesson_info():
    lesson_id = request.args.get("lesson_id")
    sql = f'select * from lesson where lesson_id="{lesson_id}"'
    db=MyDatabase()
    res1 = db.query_one(sql,True)
    res1["chapter_list"]=getChapter(lesson_id=lesson_id)
    return jsonify(res1)


def getChapter(lesson_id):
    sql = f'select * from lesson_chapter where lesson_id="{lesson_id}" order by chapter_index;'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    res2 = cursor.fetchall()
    if res2:
        for item in res2:
            sql = f'select * from lesson_subchapter where chapter_id="{item["chapter_id"]}" order by subchapter_index;'
            cursor.execute(sql)
            res3 = cursor.fetchall()
            item["children"] = res3
    connect.close()
    return res2


@teacherModule.route("/get_chapter_list", methods=["GET"])
def get_chapter_list():
    lesson_id = request.args.get("lesson_id")
    res=getChapter(lesson_id=lesson_id)
    return jsonify(res)


@teacherModule.route("/add_chapter", methods=["POST", "GET"])
def add_chapter():
    lesson_id = request.form.get("lesson_id")
    chapter_index = request.form.get("chapter_index")
    title = request.form.get("title")
    sql = f'insert into lesson_chapter (lesson_id,chapter_index,title,chapter_id)' \
          f' values ("{lesson_id}","{chapter_index}","{title}",uuid());'
    print(sql)
    db=MyDatabase()
    db.curd(sql,True)
    return jsonify({
        "message": "添加成功",
        "type": "success"
    })


@teacherModule.route("/add_subchapter", methods=["POST", "GET"])
def add_subchapter():
    chapter_id=request.form.get("chapter_id")
    subchapter_index = request.form.get("subchapter_index")
    title = request.form.get("title")
    sql = f'insert into lesson_subchapter (chapter_id,subchapter_index,title,subchapter_id)' \
          f' values ("{chapter_id}","{subchapter_index}","{title}",uuid());'
    print(sql)
    db=MyDatabase()
    db.curd(sql,True)
    return jsonify({
        "message": "添加成功",
        "type": "success"
    })


@teacherModule.route("/change_chapter", methods=["POST", "GET"])
def change_chapter():
    chapter_id=request.form.get("chapter_id")
    chapter_index = request.form.get("chapter_index")
    title = request.form.get("title")
    file_id = request.form.get("file_id")
    video_id = request.form.get("video_id")
    sql = f'update lesson_chapter set chapter_index="{chapter_index}",title="{title}",' \
          f'file_id="{file_id}",video_id="{video_id}" where chapter_id="{chapter_id}";'
    print(sql)
    db=MyDatabase()
    db.curd(sql,True)
    return jsonify({
        "message": "修改成功",
        "type": "success"
    })


@teacherModule.route("/change_subchapter", methods=["POST", "GET"])
def change_subchapter():
    subchapter_id=request.form.get("subchapter_id")
    subchapter_index = request.form.get("subchapter_index")
    title = request.form.get("title")
    file_id = request.form.get("file_id")
    video_id = request.form.get("video_id")
    sql = f'update lesson_subchapter set subchapter_index="{subchapter_index}",title="{title}",' \
          f'file_id="{file_id}",video_id="{video_id}" where subchapter_id="{subchapter_id}";'
    print(sql)
    db=MyDatabase()
    db.curd(sql,True)
    return jsonify({
        "message": "修改成功",
        "type": "success"
    })


@teacherModule.route("/edit_lesson", methods=["POST", "GET"])
def edit_lesson():
    lesson_id=request.form.get("lesson_id")
    description = request.form.get("description")
    lesson_name = request.form.get("lesson_name")
    sql1 = f'update lesson set lesson_name="{lesson_name}" where lesson_id="{lesson_id}";'
    if type(description) is str:
            description = escape_string(description)
    sql2 = f'update lesson set description="{description}" where lesson_id="{lesson_id}";'
    print(sql2)
    db=MyDatabase()
    db.curd(sql1)
    db.curd(sql2,True)
    return jsonify({
        "message": "上传成功",
        "type": "success"
    })


@teacherModule.route("/change_lesson_cover", methods=["POST", "GET"])
def change_lesson_cover():
    lesson_id=request.form.get("lesson_id")
    cover_id = request.form.get("cover_id")
    sql = f'update lesson set cover_id="{cover_id}" ' \
          f'where lesson_id="{lesson_id}";'
    print(sql)
    db=MyDatabase()
    db.curd(sql,True)
    return jsonify({
        "message": "上传封面成功",
        "type": "success"
    })


@teacherModule.route("/get_student_assignments", methods=["POST", "GET"])
def get_student_assignments():
    class_id=request.args.get("class_id")
    student_id = request.args.get("student_id")
    sql = f'select * from assignment_a where class_id="{class_id}" and ' \
          f'student_id="{student_id}" order by post_time'
    db=MyDatabase()
    res1=db.query(sql)
    sql=f'select name from student_info where username="{student_id}"'
    res2=db.query_one(sql)
    print(res2)
    for item in res1:
        item["name"]=res2["name"]
        sql=f'select title from assignment_q where id="{item["assignment_id"]}"'
        res3=db.query_one(sql)
        item["title"]=res3["title"]
        item["post_time"]=str(item["post_time"].date())
    return jsonify(res1)


@teacherModule.route("/delete_chapter",methods=["POST"])
def delete_chapter():
    chapter_id=request.form.get("id")
    db=MyDatabase()
    sql1=f'delete from lesson_chapter where chapter_id="{chapter_id}"'
    sql2=f'delete from lesson_subchapter where chapter_id="{chapter_id}"'
    try:
        db.curd(sql1)
        db.curd(sql2,True)
    except ValueError:
        print(ValueError)
    return jsonify({"type":"success","message":"OK"})


@teacherModule.route("/delete_subchapter",methods=["POST"])
def delete_subchapter():
    subchapter_id=request.form.get("id")
    db=MyDatabase()
    sql=f'delete from lesson_subchapter where subchapter_id="{subchapter_id}"'
    try:
        db.curd(sql,True)
    except ValueError:
        print(ValueError)
    return jsonify({"type":"success","message":"OK"})
