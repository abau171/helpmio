import helpmio.web
import tornado.ioloop


def main():
    helpmio.web.init(9009)
    tornado.ioloop.IOLoop.current().start()
