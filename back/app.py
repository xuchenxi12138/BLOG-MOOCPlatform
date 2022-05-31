

# flask 模块只能做个课设用，它不能解决sql注入问题，因为它没有preparestatement
# 如果对传入的字符串有处理，也算是防止sql注入的一种方式


from database import MyDatabase
from flask import Flask, jsonify, request, render_template, make_response, send_file
from flask_cors import CORS
from controller.admin import adminModule
from controller.home import homeModule
from controller.student import studentModule
from controller.teacher import teacherModule
from controller.file import fileModule
from controller.blog import blog
# cors 用于解决跨域问题
# from werkzeug.utils import secure_filename

app = Flask(__name__)
app.register_blueprint(adminModule, url_prefix='/admin')
app.register_blueprint(homeModule, url_prefix='/home')
app.register_blueprint(teacherModule, url_prefix='/teacher')
app.register_blueprint(studentModule,url_prefix='/student')
app.register_blueprint(fileModule, url_prefix='/file')
app.register_blueprint(blog, url_prefix='/blog')
CORS(app, supports_credentials=True)


@app.route('/')
def index():
    return "hello world"
    # return "OK"


# 登录模块
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    username = request.args.get('username')
    password = request.args.get('password')
    identification = request.args.get("identification")
    sql = f'select password from {identification} where username="{username}"'
    db=MyDatabase()
    result=db.query_one(sql,True)
    response = {}
    if result:
        if result["password"] == password:
            response = {
                "result": "success",
                "message": "登录成功！",
                "type": "success"
            }
        else:
            response = {
                "result": "failed",
                "message": "密码错误！",
                "type": "error"
            }
    else:
        response = {
            "result": "failed",
            "message": "用户名错误！",
            "type": "error"
        }
    return jsonify(response)


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = request.args.get('username')
    password = request.args.get('password')
    identification = request.args.get("identification")
    sql = f'select password from {identification} where username="{username}";'
    db=MyDatabase()
    result=db.query_one(sql,True)
    response = {}
    if result:
        if result["password"] == password:
            response = {
                "result": "success",
                "message": "登录成功！",
                "type": "success"
            }
        else:
            response = {
                "result": "failed",
                "message": "用户名或密码错误！",
                "type": "error"
            }
    else:
        response = {
            "result": "failed",
            "message": "用户名或密码错误！",
            "type": "error"
        }
    return jsonify(response)


@app.route('/check_cookie', methods=['GET','POST'])
def check_cookie():
    username = request.args.get('username')
    password = request.args.get('password')
    identification = request.args.get("identification")
    response = {}
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    print(username,password,identification)
    if username and password and identification:
        sql = f'select * from {identification} where username="{username}" and password="{password}";'
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            sql = f'select * from {identification}_info where username="{username}"'
            cursor.execute(sql)
            res = cursor.fetchone()
            response = {
                "result": "success",
                "full_name": res['family_name'] + res["given_name"],
                "nickname": res['nickname'],
                "avatar": res["avatar"]
            }
        else:
            response = {
                "result": "failed",
            }
    connect.close()
    return jsonify(response)


@app.route('/test', methods=['GET', "POST"])
def test():
    data = {
        "error": 0,
        "data": [
            {
                "url": "hello",
                "alt": "图片文字说明",
                "href": "跳转链接"
            }
        ]
    }
    # 返回图片地址
    return jsonify(data)


@app.route('/get_avatar', methods=['GET',"POST"])
def get_avatar():
    username=request.args.get("username")
    identification=request.args.get("identification")
    # 返回图片地址
    sql=f'select avatar,name,signature from {identification}_info where username="{username}"'
    print(sql)
    db=MyDatabase()
    result=db.query_one(sql,True)
    if result:
        if result["avatar"]:
            result["avatar"]= result["avatar"]
        else: result["avatar"]=""
    else: result={
        "avatar":"",
        "signature":"",
        "name":""
    }
    return jsonify(result)


@app.route('/search/blog',methods=['GET'])
def search_blog():
    username=request.args.get("username")
    text=request.args.get("text")
    start = request.args.get("start")
    end = int(start) + 10
    arr=text.split(" ")
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    like="%"
    for item in arr:
        like=like+item+"%"
    sql=f'select * from blog where content_text like "{like}" limit {start},{end};'
    cursor.execute(sql)
    res=cursor.fetchall()
    for item in res:
        item["post_time"]=str(item["post_time"])
        sql = f'select avatar,nickname,name from {item["identification"]}_info where username="{item["blog_owner_id"]}"'
        cursor.execute(sql)
        result2 = cursor.fetchone()
        if result2:
            item["avatar"] = result2["avatar"]
            item["blog_owner_name"] = result2["name"]
            item["nickname"] = result2["nickname"]
        if username:
            sql = f'select * from like_table where username="{username}" and work_id="{item["blog_id"]}"'
            cursor.execute(sql)
            result3 = cursor.rowcount
            if result3:
                item["liked"] = True
    sql = f'select count(*) from blog where content_text like "{like}";'
    cursor.execute(sql)
    total = cursor.fetchone()["count(*)"]
    connect.close()
    return jsonify({"total": total, "list": res})

@app.route('/search/lesson',methods=['GET'])
def search_lesson():
    text=request.args.get("text")
    start=request.args.get("start")
    end=int(start)+10
    arr=text.split(" ")
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    like="%"
    for item in arr:
        like=like+item+"%"
    sql=f'select * from lesson where lesson_name like "{like}" limit {start},{end};'
    cursor.execute(sql)
    res = cursor.fetchall()
    sql=f'select count(*) from lesson where lesson_name like "{like}";'
    cursor.execute(sql)
    total=cursor.fetchone()["count(*)"]
    connect.close()
    return jsonify({"total":total,"list":res})


if __name__ == '__main__':
    app.run(host="0.0.0.0")
