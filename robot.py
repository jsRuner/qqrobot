#!/usr/bin/env python
# encoding: utf-8

import time
import re
import urllib
import urllib2
import json
import random
import logging
import ConfigParser
from selenium import webdriver
from urllib import quote
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC  # available since 2.26.0


"""
@version: 1.0
@author: hiphp
@license: Apache Licence 
@contact: hi_php@163.com
@site: wuwenfu.cn
@software: PyCharm Community Edition
@file: robot.py
@time: 2016/1/12 20:15

qq机器人。

启动浏览器。等待扫描。

等待选择框。

获取信息。

根据信息。执行不同的命令


1、翻译

2、图灵的接口

3、表情

4、其他命令

"""
DEBUG = False

ISOPEN = True #默认开启机器人






def openBrower():
    print(u"启动浏览中...")

    # driver = webdriver.Firefox()
    # driver = webdriver.Ie()
    driver = webdriver.Chrome()
    return driver

def openQQ(driver):
    driver.get("http://w.qq.com/")
    print(u"请用手机qq扫描二维码...")

def isQQLogin(driver):
    loginstr = 'if(document.body.innerHTML.indexOf("联系人")>0 ){return 1;}else{return 2;}'
    rs = driver.execute_script(loginstr)
    if rs == 1:
        # 登录了
        print(u"扫描成功")
        return  True
    else:
        # 没有登录
        return False

def toWho(driver):
    while True:
        loginstr = "if(document.getElementById('panelTitle-5') != null ) {return document.getElementById('panelTitle-5').innerHTML;}else{return 2;}"
        rs = driver.execute_script(loginstr)
        if rs ==2:
            pass
        else:
            print(u"当前聊天对象是:%s" % rs)
            break
    return rs
# 返回当前除了自己之外的信息数量。
def getBuddymsgnum(driver):
    jsstr = 'var buddy = document.getElementsByClassName("buddy"); return buddy.length;'
    return driver.execute_script(jsstr)


# 是否有新的发言。对比2次信息的数量。相等则表示没有。不想等则有真与假
def isHaveNewmsg(driver,prevmsgnum):
    currentnum = getBuddymsgnum(driver)
    if prevmsgnum == currentnum:
        return False
    else:
        return True

# 获得最后一条除自己之外的信息。未过滤的信息。
def getLastMsg(driver):
    msg = driver.execute_script(
            'var buddys = document.getElementsByClassName("buddy");var last = buddys[buddys.length-1];return last.children[2].innerHTML;')
    print(u"原始的信息:%s" % msg)
    return msg


#处理信息。提取中文
def fetchZw(msg):
    xx = u'[\u4e00-\u9fa5]'
    pattern = re.compile(xx)
    results = pattern.findall(msg)
    return "".join(results)

# 提取其中的英文
def fetchEn(msg):
    pass

# 调用图灵接口
def tulingapi(msg):
    d = {'key': '131c04727a5deef01c1146b76fac51c5', 'info': msg.encode('utf-8')}  # 发送一次请求。获取图灵的回复。
    f = urllib.urlopen("http://www.tuling123.com/openapi/api?" + urllib.urlencode(d))
    s = f.read()
    tuling = json.loads(s)
    if tuling['code'] == 100000:
        sendinfo = u"%s" % tuling['text']
    elif tuling['code'] == 200000:
        sendinfo = u"%s链接%s" % (tuling['text'], tuling['url'])
    elif tuling['code'] == 302000:
        sendinfo = u"%s:" % (tuling['text'])
        # 新闻list  只读取一部分。3条即可。
        newsnum = 0
        for item in tuling['list']:
            if newsnum >= 3:
                break
            newsnum = newsnum + 1
            sendinfo = sendinfo + u"%s:%s" % (item['article'], item['detailurl'])
    else:
        sendinfo = u"聊点其他的吧。看不懂你们说的啥"
    return  sendinfo

def subString(string,length):
    if length >= len(string):
        return string
    result = ''
    i = 0
    p = 0
    while True:
        ch = ord(string[i])
        # 1111110x
        if ch >= 252:
            p = p + 6
        # 111110xx
        elif ch >= 248:
            p = p + 5
        # 11110xxx
        elif ch >= 240:
            p = p + 4
        # 1110xxxx
        elif ch >= 224:
            p = p + 3
        # 110xxxxx
        elif ch >= 192:
            p = p + 2
        else:
            p = p + 1

        if p >= length:
            pass
            break;
        else:
            i = p
    return string[i:]




def fanyi(f,t,info):
    msg = ""
    try:
        url = 'http://apis.baidu.com/apistore/tranlateservice/translate?from=%s&to=%s&query=%s' % (f,t,info)
        req = urllib2.Request(url)
        req.add_header("apikey", "b5d6bd8453559da98d0d0ebf87622d8a")
        resp = urllib2.urlopen(req)
        content = resp.read()
        if content:
            print(content)
            rs = json.loads(content)
            print(rs)
            if rs['errNum'] == 0:
                msg = rs['retData']['trans_result'][0]
                print(msg)
                msg = rs['retData']['trans_result'][0]['dst']
                print(msg)
        return u"翻译的结果:%s" % msg
    except Exception, e:
        print(e)
        return u"不好意思，我翻译没有那么快"

# 查询战绩
def lol(sn,pn):
    msg = ""
    try:
        d = {'serverName': sn, 'playerName': pn}  # 发送一次请求。获取图灵的回复。
        f = urllib.urlopen(" http://lolbox.duowan.com/playerDetail.php?" + urllib.urlencode(d))
        content = f.read()
        if content:
            # print(content)
            # 提取等级 战斗力 被赞 被拉黑。
            # pattern = re.compile('<em><span title=.*?>(.*?)</span></em>');
            pattern = re.compile('<div class="intro">.*?<em>(.*?)</em>.*?<div title.*?>(.*?)</div>.*?<div title.*?>(.*?)</div>.*?<em><span title=.*?>(.*?)</span></em>.*?</div>',re.S);
            result = re.findall(pattern,content)
            if result:
                print(result[0])
                for item in result[0]:
                    print(item)
                    #filter(str.isdigit, '123ab45')
                msg = "%s(%s)英雄联盟信息:等级%s,战斗力%s,被赞次数%s,被拉黑%s" % (pn,sn,result[0][0],result[0][3],filter(str.isdigit,result[0][1]),filter(str.isdigit,result[0][2]))
                print(msg)
        return "查询的结果:" + msg
    except Exception, e:
        print(e)
        return u"不好意思，查询没有那么快"

# 查询大区 http://lolbox.duowan.com/playerList.php  keyWords
def lollist(pn):
    msg = ""
    try:
        d = {'keyWords': pn}  # 发送一次请求
        f = urllib.urlopen("http://lolbox.duowan.com/playerList.php?" + urllib.urlencode(d))
        content = f.read()
        if content:
            # print(content)
            # exit()
            # 提取等级 战斗力 被赞 被拉黑。
            # pattern = re.compile('<em><span title=.*?>(.*?)</span></em>');
            pattern = re.compile('<td.*>.*?<td >(.*?)</td>.*?<td >(.*?)</td>.*?</tr>',re.S);
            result = re.findall(pattern,content)
            if result:
                print(result[0])
                # exit()
                lolliststr = ""
                for item in result[0]:
                    print(item)
                    lolliststr = lolliststr + "【"+item+"】"
                msg = "找到"+str(len(result[0]))+"条记录:" + lolliststr
                print(msg)
        return "查询的结果:" + msg
    except Exception, e:
        print(e)
    return u"不好意思，查询没有那么快"



def fanyan(driver,msg):
    try:
        driver.find_element_by_id("chat_textarea").send_keys(msg)
        time.sleep(2)
        driver.find_element_by_id("send_chat_btn").click()
    except Exception,e:
        print(e)


def main():

    global ISOPEN
    # 打开浏览器
    driver = openBrower()
    # 访问网页qq
    openQQ(driver)
    # 登录判断。
    while True:
        if isQQLogin(driver):
            break
        else:
            pass
    # 登录成功。等待选择聊天框
    toWho(driver)
    # 进入发言准备
    prevmsgnum = 0
    while True:

        if isHaveNewmsg(driver,prevmsgnum):
            # 改变当前发言的数量。下一次使用。
            prevmsgnum = getBuddymsgnum(driver)
            # 获取发言的信息。最后一条。
            msg = getLastMsg(driver)

            # 来了新消息。判断当前的机器人的开关
            if msg.startswith(u"关闭机器人"):
                ISOPEN = False
            if msg.startswith(u"启动机器人"):
                ISOPEN = True

            # 如果是关闭的则进入下一次循环
            if ISOPEN:
                pass
            else:
                continue
            # 解析信息。进行处理。

            # 翻译指令。
            if msg.startswith(u"中英"):
                # 先去掉中英.
                msg = msg.replace(u'中英','')
                print(u"待翻译的信息:"+msg)
                msg = fanyi('zh','en',msg.encode('utf-8'))
                print(msg)

            elif msg.startswith(u"英中"):
                msg = msg.replace(u'英中',' ')
                print(u"待翻译的信息:"+msg)
                msg = fanyi('en','zh',msg.encode('utf-8'))

            elif msg.startswith(u"中日"):
                msg = msg.replace(u'中日',' ')
                print(u"待翻译的信息:"+msg)
                msg = fanyi('zh','jp',msg.encode('utf-8'))

            elif msg.startswith(u"日中"):
                msg = msg.replace(u'日中',' ')
                print(u"待翻译的信息:"+msg)
                msg = fanyi('jp','zh',msg.encode('utf-8'))

            elif msg.startswith(u"中韩"):
                msg = msg.replace(u'中韩',' ')
                print(u"待翻译的信息:"+msg)
                msg = fanyi('zh','kor',msg.encode('utf-8'))

            elif msg.startswith(u"中法"):
                msg = msg.replace(u'中法',' ')
                print(u"待翻译的信息:"+msg)
                msg = fanyi('zh','fra',msg.encode('utf-8'))

            elif msg.startswith(u"白古"):
                msg = msg.replace(u'白古',' ')
                print(u"待翻译的信息:"+msg)
                msg = fanyi('zh','wyw',msg.encode('utf-8'))


            elif msg.startswith(u"古白"):
                msg = msg.replace(u'古白',' ')
                print(u"待翻译的信息:"+msg)
                msg = fanyi('wyw','zh',msg.encode('utf-8'))

            elif msg.startswith(u"lollist"):
                msg = msg.replace(u'lollist',' ')
                print(u"待查询的信息:"+msg)
                msg = lollist(msg.encode('utf-8'))
                print(msg)
                # msg = msg.encode("utf8","ignore")

            elif msg.startswith(u"lol"):
                msg = msg.replace(u'lol',' ')
                print(u"待查询的信息:"+msg)
                # 分割字符串。
                msginfo = msg.split("#")
                msg = lol(msginfo[0].encode('utf-8'),msginfo[1].encode('utf-8'))
                # msg = msg.encode("utf8","ignore")

            # 进入图灵的指令
            else:
                msg = tulingapi(msg)
            # 发送
            fanyan(driver,msg)
        else:
            # 没有

            pass
class Main():
    def __init__(self):
        pass


if __name__ == '__main__':

    # msg = fanyi('en','zh',"中国")
    # print(msg)

    # msg = "皮城警备#hiphp"
    # msginfo = msg.split("#")
    # msg = lol(msginfo[0],msginfo[1])
    # print(msg)

    # msg = "hiphp"
    # msg = lollist(msg)
    # print(msg)

    print('本程序的查询结果可能会引起一些心理上的不适,请小心使用...')
    print('回车键继续...')
    try:
        raw_input()
        input = raw_input
    except:

        input()
    main()

    print('回车键结束')
    input()
    pass