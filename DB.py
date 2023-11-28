# DB.py
# -*- coding: utf-8 -*-
import pymysql


class Database():
    def __init__(self):
        self.db = pymysql.connect(host='localhost', port=3306, user='test', passwd='jjh3733990!', db='test',
                                  charset='utf8')
        self.cursor = self.db.cursor()

    def show(self):
        sql = """SELECT * from sensor"""
        self.cursor.execute(sql)
        resurlt = self.cursor.fetchall()
        return(resurlt)

    def insert(self, date, hum, temper):
        sql = """insert into sensor values (%s, %s, %s)"""
        self.cursor.execute(sql, (date, hum, temper))
        self.db.commit()

    def show_realtime(self):
        sql = """SELECT * FROM realtime"""
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def update_realtime(self, date, hum, temper):
        sql = """UPDATE realtime SET date=%s, hum=%s, temper=%s WHERE id=1"""
        self.cursor.execute(sql, (date, hum, temper))
        self.db.commit()

    def insert_realtime(self, date, hum, temper):
        sql = """INSERT INTO realtime (date, hum, temper) VALUES (%s, %s, %s)"""
        self.cursor.execute(sql, (date, hum, temper))
        self.db.commit()

if __name__ == "__main__":
    db = Database()
    db.show()
    db.show_realtime()
