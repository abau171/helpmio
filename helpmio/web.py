import helpmio.question
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
        tornado.web.url(r"/questions/(.*)", QuestionHandler, name="question"),
        tornado.web.url(r"/ws/(.*)", QuestionWebSocketHandler, name="question_websocket"),
        tornado.web.url(r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": static_files_path}, name="static")
    ], template_path=template_path, debug=True)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(port)


def _inject_sessions(func):
    def inner(self, *args, **kwargs):
        sid = self.get_cookie("sid", None)
        session = helpmio.session.get_session(sid)
        if session is None:
            session = helpmio.session.new_session()
            self.set_cookie("sid", session.get_sid())
        self.session = session
        func(self, *args, **kwargs)
    return inner


class MainHandler(tornado.web.RequestHandler):

    @_inject_sessions
    def get(self):
        self.render("questions.html")


class NewQuestionHandler(tornado.web.RequestHandler):

    @_inject_sessions
    def get(self):
        self.render("new_question.html")

    @_inject_sessions
    def post(self):
        self.redirect(self.reverse_url("question",
            helpmio.question.new_question(
                self.get_body_argument("title"),
                self.get_body_argument("description")).get_qid()))


class QuestionHandler(tornado.web.RequestHandler):

    @_inject_sessions
    def get(self, qid):
        self.render("question.html", qid=qid)


class QuestionWebSocketHandler(tornado.websocket.WebSocketHandler):
    
    @_inject_sessions
    def open(self, qid):
        self._chatroom = helpmio.question.get_question(qid).get_chatroom()
        self._connection_id = self._chatroom.connect(self)
        def message_received(message):
            print(message)
            self.write_message(str(message))
        self._chatroom.on_chat.subscribe(message_received)

    def on_message(self, message):
        self._chatroom.add_chat(self._connection_id, message)
