# -*- coding:utf-8 -*-
import MySQLdb as mdb


def connnect_db():
    config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'passwd': 'timaimee',
        'charset': 'utf8'
    }
    conn = mdb.connect(**config)
    return conn;


def get_cursor(conn):
    cursor = conn.cursor()
    return cursor


def createDB(conn, cursor):
    DB_NAME = 'housedb'
    # cursor.execute('DROP DATABASE IF EXISTS %s' % DB_NAME)
    cursor.execute('CREATE DATABASE IF NOT EXISTS %s' % DB_NAME)
    conn.select_db(DB_NAME)


def create_table(cursor):
    # 创建数据表SQL语句
    sql = """CREATE TABLE house (
         id int primary key,
         单价  CHAR(40),
         规划用途  CHAR(40),
         非封闭阳台  CHAR(40),
         预测总面积  CHAR(40),
         项目名称  CHAR(40),
         预测套内面积  CHAR(40),
         楼栋  CHAR(40),
         房屋朝向  CHAR(40),
         是否自用  CHAR(40),
         是否抵押  CHAR(40),
         卫生间  CHAR(40),
         实测套内面积  CHAR(40),
         商品房销售价  CHAR(40),
         是否回迁  CHAR(40),
         批准销售状态  CHAR(40),
         所在楼层  CHAR(40),
         实测面积  CHAR(40),
         房屋结构  CHAR(40),
         是否查封  CHAR(40),
         房号  CHAR(40),
         实测公摊面积  CHAR(40),
         房屋户型  CHAR(40),
         层高  CHAR(40),
         封闭阳台  CHAR(40),
         厨房  CHAR(40),
         是否公建配套  CHAR(40),
         房屋功能  CHAR(40) 
       )"""
    cursor.execute(sql)


def inser_value(cursor):
    vstr = """
{"房屋功能：": "住宅", "层高：": "2.9", "房号：": "9栋22层06号房", 
"预测总面积：": "73.14", "单价": 15779, "是否回迁：": "否", 
"厨房：": "0", "封闭阳台：": "0", "房屋户型：": "一房二厅", 
"卫生间：": "1", "规划用途：": "住宅", "是否查封：": "否", 
"是否自用：": "否", "房屋结构：": "钢筋混凝土", "房屋朝向：": "南",
 "批准销售状态：": "是", "楼栋：": "9栋", "实测公摊面积：": "0.0", 
 "预测公摊面积：": "14.05", "预测套内面积：": "59.09", "商品房销售价目表(经物价部门监制)": "1154149", 
 "实测套内面积：": "0.0", "非封闭阳台：": "2", "所在楼层：": "22", "是否公建配套：": "否", 
 "项目名称：": "华浩海悦湾", "实测面积：": "0.0", "是否抵押：": "否"}
"""
    sql = """INSERT INTO house values(0,"住宅", "2.9", "9栋22层06号房", "73.14", "15779",
    "住宅", "2.9", "9栋22层06号房", "73.14", "15779",
    "住宅", "2.9", "9栋22层06号房", "73.14", "15779",
    "住宅", "2.9", "9栋22层06号房", "73.14", "15779",
    "住宅", "2.9", "9栋22层06号房", "73.14", "15779",
    "住宅", "2.9")"""
    cursor.execute(sql)


def close(conn, cursor):
    cursor.close()
    conn.close()


if __name__ == "__main__":
    print "start"
    conn = connnect_db()
    cursor = get_cursor(conn)
    createDB(conn,cursor)
    # create_table(cursor)
    print "stop"
    inser_value(cursor)
