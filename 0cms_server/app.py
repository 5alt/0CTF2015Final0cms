#!/usr/bin/env python
#coding=utf-8
import web, settings

urls = (
    '/uploads/(.*)', 'download',
    '([a-z0-9\/]*)', 'dispatcher'
    )

class dispatcher:
    def __init__(self):
        pass
    def GET(self, path):
        return self.__request(path)

    def POST(self, path):
        return self.__request(path)

    def __request(self, path=''):
        try:
            libName = 'action'
            controllerName = 'index'
            if path.count('/') < 2:
                path = settings.DEFAULT_PATH
            if path.count('/') == 2:
                modelName, controllerName = path.strip()[1:].split('/', 1)
            else:
                libName, modelName, controllerName = path.strip()[1:].split('/', 2)  
            if not modelName:
                return 'controller missing'
            moduleList = __import__(libName + '.' + modelName, {}, {}, [modelName])
            modelObj = getattr(moduleList, modelName)()
            if hasattr(modelObj, controllerName):
                result = getattr(modelObj, controllerName)()
            else:
                result = 'no such controller'
            return result
        except Exception ,e:
            from action.base import base as baseAction
            baseObj=baseAction()
            if e.message == 'db not exists' :
                return baseObj.error('To be installed',baseObj.makeUrl('install'))
            return baseObj.error(e.message,baseObj.makeUrl('index'))
            #raise Exception,e.message

class download:
    def GET(self, filepath):
        try:
            with open("./uploads/%s" % filepath, "rb") as f:
                content = f.read()
            return content
        except:
            return web.notfound("Sorry, the file you were looking for was not found.")


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()