#!/usr/bin/env python
# encoding: utf-8


import time
import urllib
import chardet
import urllib2
import json
import logging
import ConfigParser
from selenium import webdriver
from urllib import quote
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0

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


def send_message(driver,lastnum):

    # 检查一次群友说的话。如果没人说话，就说。好无聊。
    jsstr ='var buddy = document.getElementsByClassName("chat_content_group"); return buddy.length;'
    rs =  driver.execute_script(jsstr)
    # 如果为0或者数量和原来相等。没人说话。发一个好闷。来个人陪我聊天。
    if rs == 0 or rs == lastnum:
        pass
        #发送一条消息。
        # driver.find_element_by_id("chat_textarea").send_keys(u"哎呀，好无聊，谁来陪我聊聊天，我可以模仿你说话。")
        #
        # time.sleep(2)
        # driver.find_element_by_id("send_chat_btn").click()

    else:
        # 读取最后一个人的信息。并重复一次。
        # currentmsg = driver.execute_script('var buddys = document.getElementsByClassName("buddy");var last = buddys[buddys.length-1];return last.children[2].innerHTML;')
        currentmsg = driver.execute_script('var buddys = document.getElementsByClassName("chat_content_group");var last = buddys[buddys.length-1];return last.children[2].innerHTML;')

        print(currentmsg)



        print(chardet.detect(currentmsg))

        # return rs

        # currentmsg = u"%s" % currentmsg
        time.sleep(1)

        d = {'key':'131c04727a5deef01c1146b76fac51c5','info':currentmsg.encode("gbk")}
        # 发送一次请求。获取图灵的回复。
        f=urllib.urlopen("http://www.tuling123.com/openapi/api?"+urllib.urlencode(d))
        s=f.read()

        tuling = json.loads(s)

        if tuling['code'] == 100000:
            print(u"%s" % tuling['text'])
        if tuling['code'] == 200000:
            print(u"%s" % tuling['text'])
        if tuling['code'] != 100000 or tuling['code'] != 200000 :
            print(u"聊点其他的吧。看不懂你们说的啥")



        #解析json


        # driver.find_element_by_id("chat_textarea").send_keys(s)
        time.sleep(5)
        # driver.find_element_by_id("send_chat_btn").click()

    return rs



    pass



def func():
    pass


class Main():
    def __init__(self):
        pass


if __name__ == '__main__':
        #
        # currentmsg = u"恩" #不加u可以执行。加u报错。加u是转unicode。
        # currentmsg = currentmsg.encode("gbk")
        # print(currentmsg)
        # d = {'key':'131c04727a5deef01c1146b76fac51c5','info':currentmsg}
        # # 发送一次请求。获取图灵的回复。
        # f=urllib.urlopen("http://www.tuling123.com/openapi/api?"+urllib.urlencode(d))
        # s=f.read()
        #
        # print(s)
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

        url = "http://w.qq.com/"

        driver = webdriver.Firefox()
        # driver = webdriver.Chrome()


        driver.get(url)

        # 等待登录。
        while True:
        #    安全登录防止盗号 如果存在这个，说明没有登录。
            jsstr ='if(document.body.innerHTML.indexOf("联系人")>0 ){return 1;}else{return 2;}';
            rs =  driver.execute_script(jsstr)
            if rs ==1:
                # 登录了
                break
            else:
                # 没有登录
                pass

        # 这里肯定登录了。去点击联系人。
        driver.find_element_by_id("contact").click()
        time.sleep(5)
        #点击搜索
        driver.find_element_by_id("panelRightButton-2").click()
        time.sleep(5)
        # 填写内容。查找吴文付直播群友
        # driver.find_element_by_id("searchInput").send_keys(u"吴文付直播")
        driver.find_element_by_id("searchInput").send_keys(u"艾泽拉斯魔兽")
        time.sleep(5)
        # 选择第一个
        # driver.execute_script('$("#search_result_list li:first-child").click()')

        driver.execute_script('document.getElementById("search_result_list").children[0].click()')
        time.sleep(2)
        #发送一条消息。
        # driver.find_element_by_id("chat_textarea").send_keys(u"机器人测试:麻烦给我回复一句中文。")
        time.sleep(2)
        # driver.find_element_by_id("send_chat_btn").click()


        lastnum = 0
        # 先获取是否有网页的内容。如果有。则重复一次。如果没有，则随机说一句话。
        while True:
            lastnum = send_message(driver,lastnum)
            # 4秒检查一次。
            time.sleep(1)
