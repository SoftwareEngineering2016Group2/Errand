#!/usr/bin/python
# -*-coding:UTF-8 -*-

# author: 初行
# qq: 121866673
# mail: zxbd1016@163.com
# message: I need a python job
# time: 2014/10/5

import urllib
import urllib2
import cookielib
# cookie set
# 用来保持会话
cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

# default header
HEADER = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0',
    'Referer' : 'http://202.206.1.163/logout.do'
}

# operate method
def geturlopen(hosturl, postdata = {}, headers = HEADER):
    # encode postdata
    enpostdata = urllib.urlencode(postdata)
    # request url
    urlrequest = urllib2.Request(hosturl, enpostdata, headers)
    # open url
    urlresponse = urllib2.urlopen(urlrequest)
    # return url
    return urlresponse


def TestSelectTaskExecutor():
    print(geturlopen('http://127.0.0.1:8000/Errand/').read())
    print(geturlopen('http://127.0.0.1:8000/Errand/register', \
        {'username': '123', 'password' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/active', \
        {'username': '123', 'password' : '123', 'activecode' : '1111'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/login', \
        {'username': '123', 'password' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/responsetask', \
        {'pk' : 4}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/selecttaskexecutor', \
        {'pk' : 4, 'username' : '123'}).read())
def TestTaskSteps():
    print(geturlopen('http://127.0.0.1:8000/Errand/').read())
    print(geturlopen('http://127.0.0.1:8000/Errand/register', \
        {'username': '123', 'password' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/active', \
        {'username': '123', 'password' : '123', 'activecode' : '1111'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/login', \
        {'username': '123', 'password' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/responsetask', \
        {'pk' : 34}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/selecttaskexecutor', \
        {'pk' : 34, 'username' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/closetask', \
        {'pk' : 34}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/commenttask', \
        {'pk' : 34, 'comment' : 'Very Good', 'score' : 5}).read())
def TestTaskAddChangeRemove():
    print(geturlopen('http://127.0.0.1:8000/Errand/').read())
    print(geturlopen('http://127.0.0.1:8000/Errand/register', \
        {'username': '123', 'password' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/active', \
        {'username': '123', 'password' : '123', 'activecode' : '1111'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/login', \
        {'username': '123', 'password' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/changetask', \
        {'pk' : 29, 'headline': 'dai fan', 'detail' : 'dai fan', 'reward' : '5 yuan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/removetask', \
        {'pk' : 29}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/responsetask', \
        {'pk' : 30}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/selecttaskexecutor', \
        {'pk' : 30, 'username' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/changetask', \
        {'pk' : 30, 'headline': 'dai fan', 'detail' : 'dai fan', 'reward' : '5 yuan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/removetask', \
        {'pk' : 30}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/closetask', \
        {'pk' : 30}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/commenttask', \
        {'pk' : 30, 'comment' : 'Very Good', 'score' : 5}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/changetask', \
        {'pk' : 30, 'headline': 'dai fan', 'detail' : 'dai fan', 'reward' : '5 yuan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/removetask', \
        {'pk' : 30}).read())

def TestBrowseAllTask():
    print(geturlopen('http://127.0.0.1:8000/Errand/').read())
    print(geturlopen('http://127.0.0.1:8000/Errand/register', \
        {'username': '123', 'password' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/active', \
        {'username': '123', 'password' : '123', 'activecode' : '1111'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/login', \
        {'username': '123', 'password' : '123'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/browsealltask', \
        {'pk' : 100}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
        {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
    print(geturlopen('http://127.0.0.1:8000/Errand/browsealltask', \
        {'pk' : 100}).read())


#TestSelectTaskExecutor()
TestTaskSteps()
#TestTaskAddChangeRemove()
#TestBrowseAllTask()

'''
print(geturlopen('http://127.0.0.1:8000/Errand/').read())
print(geturlopen('http://127.0.0.1:8000/Errand/register', \
    {'username': '123', 'password' : '123'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/active', \
    {'username': '123', 'password' : '123', 'activecode' : '1111'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/getuserinfo').read())
print(geturlopen('http://127.0.0.1:8000/Errand/login', \
    {'username': '123', 'password' : '123'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/getuserinfo').read())
print(geturlopen('http://127.0.0.1:8000/Errand/changeuserinfo', \
    {'nickname': 'Jackson', 'sex' : 'M', 'phone_number' : '13088888888', 'birthday' : '1994-10-11', 'signature' : 'aaaa'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/getuserinfo').read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
    {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtaskaction', \
    {'pk': 12, 'start_time' : '2016-10-11 12:00:00', 'end_time' : '2016-10-11 13:00:00', 'place' : 'er jiao', 'action' : 'gei wo '}).read())





print(geturlopen('http://127.0.0.1:8000/Errand/').read())
print(geturlopen('http://127.0.0.1:8000/Errand/register', \
    {'username': '123', 'password' : '123'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/active', \
    {'username': '123', 'password' : '123', 'activecode' : '1111'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/login', \
    {'username': '123', 'password' : '123'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
    {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtaskaction', \
    {'pk': 21, 'start_time' : '2016-10-11 12:00:00', 'end_time' : '2016-10-11 13:00:00', 'place' : 'er jiao', 'action' : 'gei wo '}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/logout').read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
    {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/').read())
print(geturlopen('http://127.0.0.1:8000/Errand/register', \
    {'username': '456', 'password' : '456'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/active', \
    {'username': '456', 'password' : '456', 'activecode' : '1111'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/login', \
    {'username': '456', 'password' : '456'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtaskaction', \
    {'pk': 21, 'start_time' : '2016-10-11 12:00:00', 'end_time' : '2016-10-11 13:00:00', 'place' : 'er jiao', 'action' : 'gei wo '}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/logout').read())



print(geturlopen('http://127.0.0.1:8000/Errand/').read())
print(geturlopen('http://127.0.0.1:8000/Errand/register', \
    {'username': '123', 'password' : '123'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/active', \
    {'username': '123', 'password' : '123', 'activecode' : '1111'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/login', \
    {'username': '123', 'password' : '123'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
    {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtaskaction', \
    {'pk': 38, 'start_time' : '2016-10-11 12:00:00', 'end_time' : '2016-10-11 13:00:00', 'place' : 'er jiao', 'action' : 'gei wo'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/changetaskaction', \
    {'pk': 21, 'start_time' : '2016-10-11 13:00:00', 'end_time' : '2016-10-11 14:00:00', 'place' : 'yi jiao', 'action' : 'gei ni'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/removetaskaction', \
    {'pk': 21}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/logout').read())




print(geturlopen('http://127.0.0.1:8000/Errand/').read())
print(geturlopen('http://127.0.0.1:8000/Errand/register', \
    {'username': '123', 'password' : '123'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/active', \
    {'username': '123', 'password' : '123', 'activecode' : '1111'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/login', \
    {'username': '123', 'password' : '123'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtask', \
    {'headline': 'qu kuai di', 'detail' : 'qkd', 'reward' : 'ji tui fan'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtaskaction', \
    {'pk': 33, 'start_time' : '2016-10-11 12:00:00', 'end_time' : '2016-10-11 13:00:00', 'place' : 'er jiao', 'action' : 'gei wo'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/addtaskaction', \
    {'pk': 33, 'start_time' : '2016-10-11 12:00:00', 'end_time' : '2016-10-11 13:00:00', 'place' : 'er jiao', 'action' : 'gei wo'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/responsetask', \
    {'pk' : 33}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/changetaskaction', \
    {'pk': 27, 'start_time' : '2016-10-11 13:00:00', 'end_time' : '2016-10-11 14:00:00', 'place' : 'yi jiao', 'action' : 'gei ni'}).read())
print(geturlopen('http://127.0.0.1:8000/Errand/removetaskaction', \
    {'pk': 27}).read())'''

