# -*- coding: utf-8 -*-
#!/usr/bin/env python
#coding=utf-8
import web
from model.db.database import *
from action.base import base as baseAction
class install(baseAction):
    def __init__(self):
        baseAction.__init__(self)
        settings = self.getSettings()
        self.assignTplDir(settings.ADMIN_TPL_DIR)
    def index(self):
        return '''<a href="/install/do">click to install</a>'''
    def do(self):
        dbFilePath = settings.DB_STRING
        if os.path.exists(dbFilePath):
            return web.seeother('/')
        else:
            self.conn = db.connect(dbFilePath)
            self.cursor = self.conn.cursor()
            sqlList = ["""
            CREATE TABLE 'comment' (
            'id' INTEGER PRIMARY KEY,
            'cmsId' INT, 'name' VARCHAR(32),
            'email' VARCHAR(64),
            'content' TEXT, 'ip' VARCHAR(16) ,
            'createTime' TIMESTAMP ,
            'status' INT
            );

            """,
            """
            CREATE TABLE 'cms' (
            'id' INTEGER PRIMARY KEY,
            'name' VARCHAR(120),
            'content' TEXT,
            'commentCount' INT,
            'orders' INT,
            'views' INT,
            'createTime' TIMESTAMP,
            'status' INT
            );

            """,
            """
            CREATE TABLE 'flag' (
            'flag' TEXT PRIMARY KEY
            );
            """,
            """
            INSERT INTO flag(flag) VALUES('0ctf{md5_salt}')
            """
            ]
            for sql in sqlList:
                status = self.cursor.execute(sql)
            self.conn.commit()
        if status:
            return self.success('success',self.makeUrl('index'))
        else:
            return self.success('failed')