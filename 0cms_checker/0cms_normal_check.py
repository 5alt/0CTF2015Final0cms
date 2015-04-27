# -*- coding: utf-8 -*-
import requests
import random
import re
import string
import rsa

service = '0cms'
timeout = 10                    # define timeout here
author = 'md5_salt'         # author

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

def genRandomWord():
	word_list = ["join the student union select the department where you like to stay in",
	"this script will alert 1 onload",
	"haha you are (rm -rf /)ed",
	"important notice, system eval user data is not allowed"]
	return random.choice(word_list)
def genRandomLetters(length):
	return ''.join([random.choice(string.letters) for i in xrange(length)])

def exploit(host, port):
	url = 'http://'+host+':8080'
	headers = {'User-Agent':genRandomUserAgent()}

	r = requests.get(url, headers=headers).text

	if not 'md5_salt' in r:
		return 'access index error'

	pattern = '<h2><a href=\".*id=(?P<id>.*)\">'
	search = re.compile(pattern).search(r)

	if not search:
		with open('private.pem') as privatefile:
			p = privatefile.read()
			privkey = rsa.PrivateKey.load_pkcs1(p)
		#add a post
		crypto = requests.get('http://'+host+':8080/flag/crypto', headers=headers).text
		data = rsa.decrypt(crypto.decode('base64'), privkey)

		if len(data.split('|')) != 2:
			return 'get admin/pass error'
		(username, password) = tuple(data.split('|',2))

		#check login
		s = requests.Session()
		payload={'username':username, 'password':password}
		url = 'http://'+host+':8080/admin/check'
		if not 'success' in s.post(url, payload, headers=headers).text:
			return 'login check error'

		#check add post
		post_name = genRandomLetters(10)
		post_content = genRandomWord()+', only for test'
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
	else:
		postid = search.group('id')

	#check comment
	#name=sa&email=as%40dsc.com&content=asdsad&cmsId=6
	comment_name = genRandomLetters(10)
	comment_content = genRandomWord()
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

	return 'OK'

if __name__ == '__main__':
	print exploit('127.0.0.1', 8080)
