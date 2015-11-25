# coding=utf-8

import time
import threading
import tornado.httpserver
import tornado.ioloop
import tornado.options
from crawler import Crawler
from webserver import get_application


def start_web_server():
    tornado.options.parse_command_line()
    application = get_application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.current().start()


def main():
    threading.Thread(target=start_web_server).start()
    crawler_robot = Crawler()
    threading.Thread(target=crawler_robot.start).start()

    topic_list = [u"知乎", u"程序猿", u"最美背影女孩", u"10分钟看完琅琊榜", u"女婿上门了",u"世界还能这么玩",u"吃货在这里"]
    for tag in topic_list:
        time.sleep(5)
        crawler_robot.set_topic(tag)
        topic_list += [tag]
        topic_list = topic_list[1:]


if __name__ == '__main__':
    main()
