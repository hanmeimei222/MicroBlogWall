# coding=utf-8

import logging
import os

import tornado.web
import tornado.websocket


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class SocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def open(self):
        logging.info("open called")
        SocketHandler.waiters.add(self)

    def on_close(self):
        logging.info("closed called")
        SocketHandler.waiters.remove(self)

    @classmethod
    def send_news(cls, update_ret):
        logging.info("send_news called")
        for waiter in cls.waiters:
            waiter.write_message(update_ret)


def get_application():
    return tornado.web.Application(
        handlers=[
            (r'/', MainHandler),
            (r'/soc', SocketHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")
    )
