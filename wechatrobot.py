#!/usr/bin/env python
# encoding: utf-8


import time
import re
import random
import urllib
# import chardet
import urllib2
import json
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
@file: qqboot.py
@time: 2016/1/10 10:34

$("#panelBody-6 div:last-child >.chat_nick").innerHTML



"""


#
# 为了避免问题。这里读取信息，当前是只读取最后一条信息。
#
# 一次读取多条信息。取最后3条进行回复。
#
#

def send_message(driver, lastnum):
    # 检查一次群友说的话。如果没人说话，就说。好无聊。
    # jsstr = 'var buddy = document.getElementsByClassName("chat_content_group"); return buddy.length;'
    # jsstr = 'var buddy = document.getElementsByClassName("plain"); return buddy.length;'
    # 判断是否群友说话。如果有则执行一次。这里还需要判断是否是文本，表情的不算。
    jsstr = 'var buddy = document.getElementsByClassName("you"); return buddy.length;'



    rs = driver.execute_script(jsstr)
    # 如果为0或者数量和原来相等。没人说话。发一个好闷。来个人陪我聊天。
    if rs <= lastnum:
        pass
        # 发送一条消息。
        # driver.find_element_by_id("chat_textarea").send_keys(u"哎呀，好无聊，谁来陪我聊聊天，我可以模仿你说话。")
        #
        # time.sleep(2)
        # driver.find_element_by_id("send_chat_btn").click()

    else:
        # 读取最后一个人的信息。并重复一次。
        # currentmsg = driver.execute_script('var plains = document.getElementsByClassName("plain"); var lastplain = plains[plains.length - 1];  return lastplain.children[0].innerHTML; ')
        currentmsg = driver.execute_script('var plains = document.getElementsByClassName("js_message_plain"); var lastplain = plains[plains.length - 1];  return lastplain.innerHTML; ')
        # currentmsg = driver.execute_script(
        #     'var buddys = document.getElementsByClassName("chat_content_group");var last = buddys[buddys.length-1];return last.children[2].innerHTML;')

        print(currentmsg)

        # 如果是表情。则重复该表情。并结束方法.不等于-1表示找到了
        # 去掉对图片的处理。
        if False:
        # if currentmsg.find("img") != -1:
            print(u"发现表情")

            # 点击表情
            # driver.execute_script('$("#tool_bar a:first-child").click();')
            # driver.execute_script('$("html body.ng-scope.ng-isolate-scope.loaded div.main div.main_inner div.ng-scope div#chatArea.box.chat.ng-scope div.box_ft.ng-scope div#tool_bar.toolbar a.web_wechat_face").click();')

            # 产生随机表情。1-100之间
            # a = random.randint(1, 101)
            #产生
            # facestr = '$(".qqface%d").click();' % a

            # driver.execute_script(facestr)


            # driver.execute_script('$("html body.ng-scope.ng-isolate-scope.loaded div.main div.main_inner div.ng-scope div#chatArea.box.chat.ng-scope div.box_ft.ng-scope div#tool_bar.toolbar a.web_wechat_face").click();')


            # time.sleep(2)
            driver.find_element_by_id("editArea").send_keys(u"不好意思，表情我还无法识别")
            time.sleep(2)
            driver.find_element_by_link_text("发送").click()
            return rs



        # temp = u"s2f程序员杂志一2d3程序员杂志二2d3程序员杂志三2d3程序员杂志四2d3"
        xx = u'[\u4e00-\u9fa5]'

        pattern = re.compile(xx)
        results = pattern.findall(currentmsg)
        newcurrentmsg = "".join(results)



        # for result in results :
        #     newcurrentmsg = newcurrentmsg
        # print(u"最后的字符串:%s" % newcurrentmsg)





        # print(chardet.detect(currentmsg))

        # return rs

        # currentmsg = u"%s" % currentmsg
        time.sleep(1)

        d = {'key': '131c04727a5deef01c1146b76fac51c5', 'info': newcurrentmsg.encode('utf-8')}
        # 发送一次请求。获取图灵的回复。
        f = urllib.urlopen("http://www.tuling123.com/openapi/api?" + urllib.urlencode(d))
        s = f.read()

        tuling = json.loads(s)
        sendinfo = ''
        print(u'返回的code是%s' % tuling['code'])
        print(u'与100000是%s' % tuling['code']== 100000)
        print(u'与100000字符串是%s' % tuling['code']== '100000')
        print(u'与200000%s' % tuling['code'] == 200000)
        print(u'与200000 字符串%s' % tuling['code'] =='200000')

        if tuling['code'] == 100000:
            print(u"%s" % tuling['text'])
            sendinfo = u"%s" % tuling['text']
        elif tuling['code'] == 200000:
            print(u"%s" % tuling['text'])
            sendinfo = u"%s链接%s" % (tuling['text'],tuling['url'])
        else:
            # print(u"聊点其他的吧。看不懂你们说的啥")
            sendinfo = u"聊点其他的吧。看不懂你们说的啥"


        driver.find_element_by_id("editArea").send_keys(sendinfo)
        time.sleep(2)
        driver.find_element_by_link_text("发送").click()

    return rs

    pass


def func():
    pass


def subString(string, length):
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
            break
        else:
            i = p
    return string[0:i]


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':

    # 读取词库
    # 存储到内存。
    # 匹配以后，进行回复。



    # temp = u"s2f程序员杂志一2d3程序员杂志二2d3程序员杂志三2d3程序员杂志四2d3"
    # xx=u'[\u4e00-\u9fa5]'
    # print(xx)
    # pattern = re.compile(xx)
    # results = pattern.findall(temp)
    # for result in results :
    #     print result
    # exit()
    #
    # currentmsg = u"北京今天天气" #不加u可以执行。加u报错。加u是转unicode。原本是\xxx 加u后编程了 \ukjfd
    # currentmsg = currentmsg
    #
    # # 2016年1月11日 这里传递出现问题。中文无法被正常解析。
    # print(currentmsg)
    # d = {'key':'131c04727a5deef01c1146b76fac51c5','info':currentmsg.encode('utf-8')}
    #
    # print(d)
    #
    # print("http://www.tuling123.com/openapi/api?"+urllib.urlencode(d))
    # # 发送一次请求。获取图灵的回复。
    # f=urllib.urlopen("http://www.tuling123.com/openapi/api?"+urllib.urlencode(d))
    # s=f.read()
    # tuling = json.loads(s)
    #
    # print(u"%s" % tuling['text'])
    # exit()

    # f=urllib.urlopen("http://www.tuling123.com/openapi/api?key=131c04727a5deef01c1146b76fac51c5&info=笑话")
    # s=f.read()
    #
    # tuling = json.loads(s)
    #
    # # 文字类
    # if tuling['code'] == 100000:
    #     print(u"%s" % tuling['text'])
    #     exit()
    # #链接类
    # if tuling['code'] == 200000:
    #     print(u"%s,具体链接是%s" % (tuling['text'],tuling['url']))
    #     exit()
    #
    #
    #
    # print(s)

    # f=urllib.urlopen("http://www.tuling123.com/openapi/api?key=131c04727a5deef01c1146b76fac51c5&info=%s" % cu)
    # s=f.read()
    # print(s)
    # exit()

    url = "http://wx.qq.com/"

    # driver = webdriver.Firefox()
    driver = webdriver.Chrome()


    driver.get(url)

    # 等待登录。
    while True:
        #    安全登录防止盗号 如果存在这个，说明没有登录。
        jsstr = 'if(document.body.innerHTML.indexOf("搜索")>0 ){return 1;}else{return 2;}';
        rs = driver.execute_script(jsstr)
        if rs == 1:
            # 登录了
            break
        else:
            # 没有登录
            pass

    time.sleep(2)
    lastnum = 0 #发送信息之前的小心数。

    while True:
        # 判断是否存在聊天的窗口。要打开聊天的窗口，很困难。这里是手动
        # 12:33:00.333 $(".title_name")[0].innerHTML
        jsstr = 'return  $(".title_name")[0].innerHTML;'
        rs = driver.execute_script(jsstr)
        # 如果不为空.则表示有聊天的窗口。


        if rs != "" :
            # 发送一条消息。
            lastnum = send_message(driver, lastnum)

            # driver.find_element_by_id("editArea").send_keys(u"你好")
            # time.sleep(2)
            # driver.find_element_by_link_text("发送").click()

            pass
        else:
            # 没有聊天窗口。
            time.sleep(3)

            pass





    # 发送一条消息。
    driver.find_element_by_id("chat_textarea").send_keys(u"你好")
    time.sleep(2)
    driver.find_element_by_id("send_chat_btn").click()


    lastnum = 0
    # 先获取是否有网页的内容。如果有。则重复一次。如果没有，则随机说一句话。
    while True:
        lastnum = send_message(driver, lastnum)
        # 4秒检查一次。
        time.sleep(2)
