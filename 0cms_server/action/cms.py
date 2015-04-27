# -*- coding: utf-8 -*-

import web,time
from action.base import base as baseAction
import model
class cms(baseAction):
    def __init__(self):
        baseAction.__init__(self)
        settings = self.getSettings()
        self.assignTplDir(settings.ADMIN_TPL_DIR)
    def save(self):
        userInput= self.getInput()
        date = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        data={
            'content':userInput['content'],
            'name':userInput['name'],
            'createTime':date,
            'status':userInput['status'],
            'orders':userInput['orders'],
            'views':0,
            'commentCount':0
        }
        status = model.cms().insert(data)
        if status:
            return self.success('save success, post id '+str(status)+'~', self.makeUrl('cms','list'))
        else:
            return self.error('save failed')
    def modify(self):
        userInput= self.getInput()
        data={
            'content':userInput['content'],
            'name':userInput['name'],
            'status':userInput['status'],
            'orders':userInput['orders'],
        }
        condition = {'id':userInput['id']}
        status = model.cms().update(data,condition)
        if status:
            return self.success('modify success',self.makeUrl('cms','list'))
        else:
            return self.error('modify failed')
    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        settings = self.getSettings()
        count = settings.PER_PAGE_COUNT
        offset= (page-1)*count if page > 0 else 0
        cmsObj = model.cms()
        condition = {}
        listData = cmsObj.getOne('COUNT(*) AS `total`',condition)
        totalCount = listData['total']
        cmsList = cmsObj.getList('*',condition,'id desc',str(offset)+','+str(count))
        self.assign('cmsList',cmsList)
        pageString = self.getPageStr(self.makeUrl('cms','list'),page,count,totalCount)
        self.assign('pageString',pageString)
        return self.display('cmsList')

    def add(self):
        return self.display('cmsAdd')
    def edit(self):
        inputParams = self.getInput()
        if not inputParams.has_key('id') :
            return self.error('not exist')
        id=inputParams['id']
        condition={'id':str(id)}
        atl=model.cms().getOne('*',condition)
        self.assign('atl',atl)
        return self.display('cmsEdit')

    def delete(self):
        inputParams = self.getInput()
        if not inputParams.has_key('id') :
            return self.error('not exist')
        id=inputParams['id']
        condition={'id':str(id)}
        result=model.cms().delete(condition)
        if result:
            return self.success('delete success',self.makeUrl('cms','list'))
        else:
            return self.error('delete failed')