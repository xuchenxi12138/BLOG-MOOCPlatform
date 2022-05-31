import json
import datetime
from flask import Blueprint, url_for, request, render_template, session, redirect, jsonify
from database import MyDatabase

# 创建了一个蓝图对象
homeModule = Blueprint('homeModule', __name__)


@homeModule.route('/', methods=["GET"])
def index():
    return 'start home module'


# @homeModule.route('/get_recommend_list', methods=["GET"])
def get_recommend_list():
    sql = "select title,url,cover_url from home_recommend_work order by time desc;"
    db=MyDatabase()
    result=db.query(sql,True)
    return result


# @homeModule.route('/get_all_lesson_list', methods=["GET"])
def get_all_lesson_list():
    sql = "select * from lesson;"
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    cursor.execute(sql)
    result = cursor.fetchall()
    response = []
    for item in result:
        if item["teacher_id"]:
            sql = f'select name from teacher_info where username="{item["teacher_id"]}";'
            cursor.execute(sql)
            res2 = cursor.fetchone()
            if res2:
                item["teacher_name"] = res2["name"]
                response.append(item)
    connect.close()
    return response


@homeModule.route('/get_start', methods=["GET"])
def get_start():
    return jsonify({"recommend_list": get_recommend_list(), "lesson_list": get_all_lesson_list()})


@homeModule.route("/get_lesson_info_by_leson_id", methods=["GET"])
def get_lesson_info():
    lesson_id = request.args.get("lesson_id")
    sql = f'select * from lesson where lesson_id="{lesson_id}"'
    db=MyDatabase()
    res1=db.query_one(sql)
    sql=f'select name from teacher_info where username="{res1["teacher_id"]}"'
    res2=db.query_one(sql,True)
    res1["teacher_name"]=res2["name"]
    res1["chapter_list"] = getChapter(lesson_id=lesson_id)
    return jsonify(res1)


def getChapter(lesson_id):
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    sql = f'select * from lesson_chapter where lesson_id="{lesson_id}" order by chapter_index;'
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


@homeModule.route("/get_lesson_info_by_subchapter_id", methods=["GET"])
def get_lesson_info_by_subchapter_id():
    lesson_id = request.args.get("lesson_id")
    subchapter_id=request.args.get("subchapter_id")
    sql = f'select * from lesson where lesson_id="{lesson_id}"'
    db=MyDatabase()
    cursor=db.cursor
    connect=db.connect
    connect.ping(reconnect=True)
    cursor.execute(sql)
    res1 = cursor.fetchone()
    res1["chapter_list"] = getChapter(lesson_id=lesson_id)
    sql=f'select name from teacher_info where username="{res1["teacher_id"]}"'
    res2=db.query_one(sql)
    res1["teacher_name"]=res2["name"]
    sql=f'select * from lesson_subchapter where subchapter_id="{subchapter_id}"'
    cursor.execute(sql)
    res2=cursor.fetchone()
    res1["subchapter_info"]=res2
    connect.close()
    return jsonify(res1)


