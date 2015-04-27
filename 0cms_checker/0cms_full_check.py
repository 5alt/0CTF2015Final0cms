# -*- coding: utf-8 -*-
import requests
import rsa
import random
import string
import re
import os
import secretagent#you need change this
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


service = '0cms'
timeout = 10					# define timeout here
author = 'md5_salt'			# author


def genRandomChars(length):
	return ''.join([random.choice(string.punctuation+string.letters) for i in xrange(length)])
def genRandomLetters(length):
	return ''.join([random.choice(string.letters) for i in xrange(length)])
def genRandomUserAgent():
    user_agent_list = [\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",\
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
       ]
    return random.choice(user_agent_list)
def getTeamID(host):
	return int(host[8:10])


def exploit(host, port):
	"""
		if the service is OK then return 'OK', other message means DOWN.
	"""
############
#  init part
############
	#not check for first 2 min
	if (int(time.time()) % 600) < 120:
		return 'OK'

	global service

	flag = secretagent.flag(service, getTeamID(host))#you need change this

	with open('private.pem') as privatefile:
		p = privatefile.read()
		privkey = rsa.PrivateKey.load_pkcs1(p)

	headers = {'User-Agent':genRandomUserAgent()}
################
#  begin check
################
	#get admin
	crypto = requests.get('http://'+host+':8080/flag/crypto', headers=headers).text
	data = rsa.decrypt(crypto.decode('base64'), privkey)

	if len(data.split('|')) != 2:
		return 'get admin/pass error'
	(username, password) = tuple(data.split('|',2))

	#check flag
	#flag = 'md5_salt'
	result = requests.get('http://'+host+':8080/flag/check?flag='+flag, headers=headers).text
	if result != '1':
		return 'check flag error'

	#check login
	s = requests.Session()
	payload={'username':username, 'password':password}
	url = 'http://'+host+':8080/admin/check'
	if not 'success' in s.post(url, payload, headers=headers).text:
		return 'login check error'

	if flag != s.get('http://'+host+':8080/flag/index', headers=headers).text:
		return 'get flag using admin error'

	#check upload
	ext = ['py', 'sh', 'php', 'txt']
	filename = genRandomLetters(10)+'.'+random.choice(ext)
	filecontent = genRandomChars(100)
	f = open(filename, 'wb')
	f.write(filecontent)
	f.close()
	files = {'uploadFile': open(filename, 'rb')}
	url = 'http://'+host+':8080/upload/upload'
	r = s.post(url, files=files, headers=headers).text
	if not 'uploads' in r:
		return 'upload file error'
	os.remove(filename)

	#get file url
	pattern = 'onclick=\"this.select\(\);\" value=\"(?P<url>.*)\" /><hr />'
	search = re.compile(pattern).search(r)
	if not search:
		return 'get file url error'

	file_url = search.group('url')
	#no admin privilege
	#url = 'http://'+host+':8080/uploads/'+filename
	url = file_url
	r = requests.get(url, headers=headers).text
	if r != filecontent:
		return 'access uploaded file error'

	#check add post
	post_name = genRandomLetters(10)
	post_content = genRandomChars(100)
	orders = 0
	status = 1
	payload = {'name':post_name, 'content':post_content, 'orders':orders, 'status':status}
	url = 'http://'+host+':8080/cms/save'
	r = s.post(url, payload, headers=headers).text
	pattern = "post id (?P<id>[0-9]+)~"
	search = re.compile(pattern).search(r)
	if not search:
		return 'get post id error'

	postid = search.group('id')
	if not 'success' in r:
		return 'post success error'

	#check post
	r = requests.get('http://'+host+':8080', headers=headers).text
	if not post_name in r:
		return 'find post name in index error'
	r = requests.get('http://'+host+':8080/index/show?id='+postid, headers=headers).text
	if not post_name in r:
		return 'get post using id error'

	#check modify
	post_name = genRandomLetters(10)
	post_content = genRandomChars(100)
	orders = 0
	status = 1
	payload = {'id':postid,'name':post_name, 'content':post_content, 'orders':orders, 'status':status}
	url = 'http://'+host+':8080/cms/modify'
	r = s.post(url, payload, headers=headers).text
	if not 'success' in r:
		return 'modify error'
	#check modify
	r = requests.get('http://'+host+':8080', headers=headers).text
	if not post_name in r:
		return 'check modify error'
	r = requests.get('http://'+host+':8080/index/show?id='+postid, headers=headers).text
	if not post_name in r:
		return 'check modify by id error'
	#check comment
	#name=sa&email=as%40dsc.com&content=asdsad&cmsId=6
	comment_name = genRandomLetters(10)
	comment_content = genRandomChars(100)
	email = genRandomLetters(5)+'@'+genRandomLetters(3)+'.com'
	payload = {'cmsId':postid,'name':comment_name, 'content':comment_content, 'email':email}
	url = 'http://'+host+':8080/index/comment'
	r = requests.post(url, payload, headers=headers).text
	pattern = "comment id (?P<id>[0-9]+)~"
	search = re.compile(pattern).search(r)
	if not search:
		return 'get comment id error'
	commentid = search.group('id')
	if not 'success' in r:
		return 'comment error'
	r = requests.get('http://'+host+':8080/index/show?id='+postid, headers=headers).text
	if not comment_name in r:
		return 'check comment error'
	#delete comment
	r = s.get('http://'+host+':8080/comment/delete?id='+commentid, headers=headers).text
	if not 'success' in r:
		return 'delete comment error'
	r = requests.get('http://'+host+':8080/index/show?id='+postid, headers=headers).text
	if comment_name in r:
		return 'check comment error'
	#delete post
	r = s.get('http://'+host+':8080/cms/delete?id='+postid, headers=headers).text
	if not 'success' in r:
		return 'delete post error'
	r = requests.get('http://'+host+':8080/index/show?id='+postid, headers=headers).text
	if post_name in r:
		return 'check delete post error'
		
	return 'OK'

if __name__ == '__main__':
	print exploit('127.0.0.1', 8080)
