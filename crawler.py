# coding=utf-8

import logging
import random
import re
import time

import requests
from bs4 import BeautifulSoup

from webserver import SocketHandler


class Crawler(object):
    # uid = u'2462430990'
    # pwd = u'hanhan0912696'
    # email = u'978288958@qq.com'

    uid = u'3272287587'
    pwd = u'0912661xyj'
    email = u'1206539220@qq.com'

    url_login_before = u'http://weibo.cn/u/' + uid
    url_login_after = u'http://login.weibo.cn/login/'
    url_search_before = u'http://weibo.cn/search/?tf=5_012'
    url_search_after = u'http://weibo.cn/search/?pos=search'
    topic = u""
    update_ret = u""
    s = None
    flag = True

    def login(self):
        """
        模拟登录
        """
        self.s = requests.Session()
        login_html = self.s.get(self.url_login_before).content
        soup = BeautifulSoup("".join(login_html))
        password = soup.find(name="input", attrs={'type': 'password'})["name"]
        vk = soup.find(name="input", attrs={'name': 'vk'})["value"]
        action = soup.find(name="form", attrs={'method': 'post'})["action"]

        login_new_url = self.url_login_after + action
        login_data = {
            'mobile': self.email,
            password: self.pwd,
            'remember': 'on',
            'backURL': self.url_login_before,
            'backTitle': u'微博',
            'tryCount': '',
            'vk': vk,
            'submit': u'登录'
        }
        self.s.post(login_new_url, data=login_data)

        logging.info(u'login success')

    def set_topic(self, topic):
        """
        设置待查询topic
        """
        self.topic = u'#' + topic + u'#'

    def get_topic_content(self):
        if self.topic == u'##':
            return SocketHandler.send_news(u"您搜索的话题没有找到相应内容噢")

        search_html = self.s.get(self.url_search_before).content
        soup = BeautifulSoup("".join(search_html))
        smblog = soup.find(name="input", attrs={'name': 'smblog'})["value"]

        search_ret_html = self.s.post(
            self.url_search_after,
            data={
                'keyword': self.topic,
                'smblog': smblog
            }
        ).content
        soup = BeautifulSoup("".join(search_ret_html))
        microlog = soup.findAll(name="div", attrs={'id': re.compile("_M*")})
        update_ret = "".join([str(tag) for tag in microlog])

        logging.info(u"content updated" + self.topic)
        if update_ret == '':
            return SocketHandler.send_news(u"您搜索的话题没有找到相应内容噢")
        SocketHandler.send_news(update_ret)

    def update_content(self):
        while self.flag:
            self.get_topic_content()
            relay = random.uniform(3, 5)
            time.sleep(relay)

    def start(self):
        self.login()
        self.update_content()
