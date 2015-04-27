# -*- coding: utf-8 -*-
#!/usr/bin/env python
import web, time,math
import settings
class base:
    tplData = {}
    globalsTplFuncs = {}
    tplDir = ''
    referer = ''
    settings = {}
    errorMessage = ''
    cookie = {}
    def __init__(self):
        self.settings = settings
        self.tplData = {
            'webTitle' : self.settings.WEB_TITLE,
            'webUrl' : self.settings.WEB_URL,
            'webDescription' : self.settings.WEB_DESCRIPTION,
            'statusList':self.settings.STATUS_LIST
        }
        self.globalsTplFuncs = {}
        self.tplDir = ''
        self.initCommonTplFunc()
        self.referer= web.ctx.env.get('HTTP_REFERER', self.settings.WEB_URL)
        self.loadCookie()

    def initCommonTplFunc(self):
        subStr=lambda strings,offset,length : self.subText(strings,offset,length)
        makeUrl= lambda action,method='index',params={} : self.makeUrl(action,method,params)
        self.assignTplFunc({'subStr':subStr,'makeUrl':makeUrl})

    def subText(self,strings,offset,length):
        return self.strip_tags(strings)[offset:length]

    def strip_tags(self,html):
        from HTMLParser import HTMLParser
        html=html.strip()
        html=html.strip("\n")
        result=[]
        parse=HTMLParser()
        parse.handle_data=result.append
        parse.feed(html)
        parse.close()
        return "".join(result)

    def assign(self,key,value=''):
        if type(key) == dict:
            self.tplData = dict(self.tplData,**key)
        else:
            self.tplData[key] = value

    def display(self,tplName):
        if self.tplDir == '':
            self.assignTplDir(settings.TEMPLATE_THEME)
        self.tplData['render'] = web.template.render(self.tplDir,globals=self.globalsTplFuncs)
        return getattr(self.tplData['render'], tplName)(self.tplData)

    def assignTplDir(self,tplDir):
        self.tplDir = settings.TPL_DIR+'/'+tplDir+'/'

    def assignTplFunc(self,funcs):
        self.globalsTplFuncs = dict(self.globalsTplFuncs,**funcs)

    def success(self,msg,url,timeout=5):
        tplData = {'msg': msg, 'url': url,'timeout':timeout}
        self.assign('jump',tplData)
        return self.display('success')

    def error(self,msg,url=None,timeout=5):
        if url ==None:
            url= web.ctx.env.get('HTTP_REFERER', self.settings.WEB_URL)
        tplData={'msg':msg,'url':url,'timeout':timeout}
        self.assign('jump',tplData)
        return self.display('error')

    def makeUrl(self,action,method='index',params={}):
        import urllib
        paramsStr = '?'+urllib.urlencode(params) if len(params)>0 else ''
        return self.settings.WEB_URL+action+'/'+method+paramsStr

    def loadCookie(self):
        if web.cookies().get('auth'):
            self.cookie = web.session.Store().decode(web.cookies().get('auth'))

    def setCookie(self):
        web.setcookie('auth', web.session.Store().encode(self.cookie), expires=86400, domain=None, secure=False)

    def isLogin(self):
        return 'login' in self.cookie and self.cookie['login'] == True

    def setLogin(self,userData=None):
        if userData == None:
            self.cookie['login'] = False
        else:
            self.cookie['login'] = True
            self.cookie['username'] = userData['username']
        self.setCookie()

    def getInput(self):
        return web.input()

    def getPageStr(self,url,currentPage,perPageCount,totalCount=10000):
        totalPage = int(math.ceil(totalCount/perPageCount))
        if '?' in url:
            url=url+'&page='
        else:
            url=url+'?page='
        pageString= ''

        if currentPage > 1:
            pageString += '''
                <span class="alignleft"><a href="'''+url+str(currentPage-1)+'''">&laquo; previous page</a></span>
            '''
        if totalPage>currentPage:
            pageString = pageString+'''
            <span class="alignright"><a href="'''+url+str(currentPage+1)+'''">next page &raquo;</a></span>
        '''
        return pageString

    def getSettings(self):
        return self.settings

    def validates(self,validList):
        userInput=self.getInput()
        for i in validList:
            if not i.validate(userInput[i.name]):
                self.errorMessage=i.note
                return False
        return True
