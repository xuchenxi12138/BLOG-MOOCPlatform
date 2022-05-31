import pymysql
import json

config=open("config.json", "r")
config = json.load(config)
class MyDatabase():
    def __init__(self) -> None:
        self.connect=pymysql.connect(
            host=config["host"],
            port=config["port"],
            database=config["database"],
            user=config["user"],
            password=config["password"])
        self.cursor=self.connect.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行更新、修改、插入操作
    # close代表是否要关闭光标
    def curd(self,sql,close=False):
        if close:
            self.cursor.execute(sql)
            self.connect.commit()
            self.connect.close()
        else: 
            self.cursor.execute(sql)
            self.connect.commit()
    # 查询一条数据
    def query_one(self,sql,close=False):
        if close:
            self.cursor.execute(sql)
            self.connect.close()
            return self.cursor.fetchone()
        else: 
            self.cursor.execute(sql)
            return self.cursor.fetchone()
    # 查询多条数据
    def query(self,sql,close=False):
        if close:
            self.cursor.execute(sql)
            self.connect.close()
            return self.cursor.fetchall()
        else: 
            self.cursor.execute(sql)
            return self.cursor.fetchall()


