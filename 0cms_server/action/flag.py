# -*- coding: utf-8 -*-
#!/usr/bin/env python
import rsa
import web
from action.base import base as baseAction
import model
class flag(baseAction):
    def __init__(self):
        baseAction.__init__(self)
        settings = self.getSettings()
        self.assignTplDir(settings.TEMPLATE_THEME)

    def index(self):
        if self.isLogin():
            flagObj = model.flag()
            realFlag = flagObj.getOne('*',{})
            return realFlag['flag']
        else:
            settings = self.getSettings()
            web.seeother(settings.WEB_URL)

    def check(self):
        #for checker
        inputParams = self.getInput()
        if not inputParams.has_key('flag') :
            settings = self.getSettings()
            web.seeother(settings.WEB_URL)
        flag = inputParams['flag']
        flagObj = model.flag()
        realFlag = flagObj.getOne('*',{})['flag']
        if realFlag == flag:
            return '1'
        else:
            return '0'

    def crypto(self):
        #for checker
        settings = self.getSettings()
        with open(settings.PUB_KEY) as publickfile:
            p = publickfile.read()
            pubkey = rsa.PublicKey.load_pkcs1(p)
        message = settings.ADMIN_USERNAME+'|'+settings.ADMIN_PASSWORD
        return rsa.encrypt(message, pubkey).encode('base64')
