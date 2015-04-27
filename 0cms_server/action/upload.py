# -*- coding: utf-8 -*-
#!/usr/bin/env python
#coding=utf-8
import web,time
from action.base import base as baseAction
import model
class upload(baseAction):
    def __init__(self):
        baseAction.__init__(self)
        if self.isLogin() != True:
            raise web.seeother('/')
        settings = self.getSettings()
        self.assignTplDir(settings.ADMIN_TPL_DIR)
    def index(self):
        return self.display('uploadFile')
    def upload(self):
        inputParams = web.input(uploadFile={})
        settings = self.getSettings()
        filedir = settings.ROOT_PATH+settings.UPLOAD_DIR 
        if 'uploadFile' in inputParams:
            fout = open(filedir +'/'+ inputParams.uploadFile.filename,'w')
            fout.write(inputParams.uploadFile.file.read())
            fout.close()
        self.assign('text',settings.WEB_URL+settings.UPLOAD_DIR+inputParams.uploadFile.filename)
        return self.display('copyText')