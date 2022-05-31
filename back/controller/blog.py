import json
import uuid

from flask import Blueprint, url_for, request, render_template, session, redirect, jsonify
# from database import cursor
from database import MyDatabase
from pymysql.converters import escape_string
blog = Blueprint('blog', __name__)


@blog.route('/get', methods=["GET"])
def get():
    blog_id = request.args.get("blog_id")
    username=request.args.get("username")
    sql = f'select * from blog where blog_id="{blog_id}"'
    sql1=f'select * from like_table where username="{username}" and work_id="{blog_id}" and type="blog"'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    response=cursor.fetchone();
    blog_owner_id =response["blog_owner_id"]
    sql2 = f'select avatar,name from {response["identification"]}_info where username="{blog_owner_id}";'
    cursor.execute(sql1)
    if cursor.rowcount:
        response["liked"]=True
    cursor.execute(sql2)
    result=cursor.fetchone()
    response["avatar"]=result["avatar"]
    response["blog_owner_name"]=result["name"]
    response["post_time"]=str(response["post_time"])
    connect.close()
    return jsonify(response)


@blog.route('/post', methods=["POST"])
def post():
    form = request.form
    identification = form["identification"]
    sql = f'select nickname from {identification}_info where username="{form["owner_id"]}"'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    result = cursor.fetchone()
    nickname = result['nickname']
    blog_id = uuid.uuid4()
    tags=escape_string(form["tags"])
    # post_time通过后台传
    sql1 = f'insert into blog (blog_id,blog_owner_id,blog_owner_name,post_time,' \
           f'title,content_text,cover,identification,tags)' \
           f'values ("{blog_id}","{form["owner_id"]}","{nickname}",now(),"{form["title"]}",' \
           f'"{form["content_text"]}","{form["cover"]}","{form["identification"]}","{tags}");'
    sql2 = "update blog set content_html='{}' where blog_id='{}'".format(form["content_html"], blog_id)

    response = {}
    try:
        cursor.execute(sql1)
        cursor.execute(sql2)
        connect.commit()
        response = {
            "type": "success",
            "message": "上传成功",
        }
    except ValueError:
        print(ValueError)
        response = {
            "type": "failed",
            "message": "访问数据库失败",
        }
    connect.close()
    return jsonify(response)

@blog.route('/change', methods=["POST"])
def change():
    form = request.form
    identification = form["identification"]
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    tags = escape_string(form["tags"])
    # post_time通过后台传
    sql1=f'update blog set post_time=now(),content_text="{form["content_text"]}",' \
        f'title="{form["title"]}",cover="{form["cover"]}",tags="{tags}"' \
        f'where blog_id="{form["blog_id"]}"'
    sql2 = "update blog set content_html='{}' where blog_id='{}'".format(form["content_html"], form['blog_id'])
    response = {}
    try:
        cursor.execute(sql1)
        cursor.execute(sql2)
        connect.commit()
        response = {
            "type": "success",
            "message": "上传成功",
        }
    except ValueError:
        print(ValueError)
        response = {
            "type": "failed",
            "message": "访问数据库失败",
        }
    connect.close()
    return jsonify(response)

@blog.route('/get_avatar', methods=["GET"])
def get_avatar():
    blog_owner_id = request.args.get("blog_owner_id")
    identification = request.args.get("identification")
    sql = f'select avatar from {identification}_info where username="{blog_owner_id}"'
    db=MyDatabase()
    avatar =db.query_one(sql,True)
    return jsonify(avatar)


@blog.route('/check_like', methods=["GET"])
def check_like():
    username = request.args.get("username")
    work_id = request.args.get("work_id")
    type=request.args.get("type")
    sql = f'select * from like_table where username="{username}" and work_id="{work_id}" and type="{type}" and state=1'
    print(sql)
    db=MyDatabase()
    result=db.query_one(sql,True)
    if(result):
        print("youzhi")
    return jsonify("OK")


@blog.route('/get_blog_list',methods=["GET"])
def get_blog_list():
    username=request.args.get("username")
    order=request.args.get("order")
    sort=request.args.get("sort")
    start=request.args.get("start")
    end=int(start)+5
    sql=f'select * from blog order by {order} {sort} limit {start},{end}'
    response={}
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    result=cursor.fetchall()
    if result:
        for item in result:
            sql=f'select avatar from {item["identification"]}_info where username="{item["blog_owner_id"]}"'
            cursor.execute(sql)
            result2=cursor.fetchone()
            if result2:
                item["avatar"]=result2["avatar"]
            if username:
                sql=f'select * from like_table where username="{username}" and work_id="{item["blog_id"]}"'
                cursor.execute(sql)
                result3=cursor.rowcount
                if result3:
                    item["liked"]=True
        response={
            "result": "success",
            "more_blog": result
        }
    else:
        response={
            "result":"noMore"
        }
    connect.close()
    return jsonify(response)

# @blog.route('/get_more_blogs',methods=["GET"])
# def get_more_blogs():
#     username=request.args.get("username")
#     order=request.args.get("order")
#     sort=request.args.get("sort")
#     sql=f'select * from blog order by {order} {sort}'
#     response={}
#     with cursor:
#         cursor.execute(sql)

@blog.route('/like', methods=["GET"])
def like():
    username = request.args.get("username")
    blog_id = request.args.get("blog_id")
    response = {}
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    # 必须登录才能执行加一
    if username:
        # 查询是否点赞过
        sql = f'select * from like_table where username="{username}" and work_id="{blog_id}"'
        cursor.execute(sql)
        result = cursor.fetchone()
        # 查询是都有相关记录
        if (cursor.rowcount > 0):
            # 如果点过就取消
            if result['state']==True:
                sql1=f'update like_table set state=false where username="{username}" and work_id="{blog_id}"'
                response["state"]=False
                cursor.execute(sql1)
                connect.commit()
            # 否则点赞
            else:
                sql1=f'update like_table set state=true where username="{username}" and work_id="{blog_id}"'
                response["state"] = True
                cursor.execute(sql1)
                connect.commit()
        else:
            # 没有记录就插入
            sql1=f'insert into like_table (username,work_id,state,type,post_time) values' \
                 f'("{username}","{blog_id}",true,"blog",now());'
            cursor.execute(sql1)
            connect.commit()
            response["state"] = True
    else:
        response["state"] = False
        response["message"] = "请先登录"
    # 没有登录都可以执行的动作
    # 查询所有点赞的记录
    sql2=f'select count(*) from like_table where username="{username}" and work_id="{blog_id}" and state=true'
    cursor.execute(sql2)
    result=cursor.fetchone()
    count=result["count(*)"]
    response["count"]=count
    # 刷新一下点赞记录
    sql3 = f'update blog set liked_number={count} where blog_id="{blog_id}"'
    cursor.execute(sql3)
    connect.commit()
    response["count"]=count
    connect.close()
    return jsonify(response)


@blog.route('/edit', methods=["POST"])
def edit():
    return "OK"


@blog.route('/delete', methods=["GET","POST"])
def delete():
    blog_id=request.args.get("blog_id")
    sql=f'delete from blog where blog_id="{blog_id}"'
    response={}
    try:
        db=MyDatabase()
        db.curd(sql,True)
        response={
            "type":"success",
            "message":"删除成功"
        }
    except ValueError:
        print(ValueError)
        response = {
            "type": "error",
            "message": "删除失败"
        }
    return jsonify(response)

