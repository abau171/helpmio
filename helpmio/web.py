import helpmio.session
import os
import tornado.httpserver
import tornado.web
import tornado.websocket

def init(port):
    template_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "assets", "templates")
    static_files_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "assets", "web")
    app = tornado.web.Application([
        tornado.web.url(r"/", MainHandler, name="main"),
        tornado.web.url(r"/questions/new", NewQuestionHandler, name="new_question"),
        tornado.web.url(r"/questions/(\d+)", QuestionHandler, name="question"),
        tornado.web.url(r"/ws", WebSocketHandler, name="websocket"),
        tornado.web.url(r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": static_files_path}, name="static")
    ], template_path=template_path, debug=True)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(port)


def _inject_sessions(func):
    def inner(self):
        sid = self.get_cookie("sid", None)
        session = helpmio.session.get_session(sid)
        if session is None:
            session = helpmio.session.new_session()
            self.set_cookie("sid", session.get_sid())
        self.session = session
        func(self)
    return inner


class MainHandler(tornado.web.RequestHandler):

    @_inject_sessions
    def get(self):
        self.render("questions.html")


class NewQuestionHandler(tornado.web.RequestHandler):

    @_inject_sessions
    def get(self):
        self.write("New Question")


class QuestionHandler(tornado.web.RequestHandler):

    @_inject_sessions
    def get(self):
        self.write("Question")


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    pass
