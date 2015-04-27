#!/usr/bin/env python
#coding=utf-8
import os

def get_local_ip(ifname): 
    import socket, fcntl, struct
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    inet = fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15])) 
    ret = socket.inet_ntoa(inet[20:24]) 
    return ret 

WEB_URL='http://'+get_local_ip('eth0')+':8080/'
WEB_TITLE='0CMS'
WEB_DESCRIPTION='0CMS Written By md5_salt'
TEMPLATE_THEME='default'
PER_PAGE_COUNT = 10

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD='salt'

DEFAULT_PATH='/index/index'
DEBUG_SWITCH=True
STATUS_LIST = {1:'publish',0:'private'}

ROOT_PATH=os.getcwd()+'/'
DATA_DIR_PATH=ROOT_PATH+'data/'
TMP_DIR_PATH=ROOT_PATH+'data/cache/'

UPLOAD_DIR='uploads/'
TPL_DIR = 'templates'
ADMIN_TPL_DIR='admin'

#cannot change
DB_TYPE='sqlite'
DB_STRING=DATA_DIR_PATH+'0ctf.db'

PUB_KEY=DATA_DIR_PATH+'public.pem'
