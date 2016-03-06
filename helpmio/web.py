import helpmio.question
import helpmio.session
import os
import tornado.httpserver
import tornado.web
import tornado.websocket
import json

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
        questions = helpmio.question.get_all_questions()
        self.render("question_list.html", questions=questions)


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
        question = helpmio.question.get_question(qid)
        self._chatroom = question.get_chatroom()
        self._connection_id = self._chatroom.connect(self)
        self._connect_cid = self._chatroom.on_connect.subscribe(self.connect_recieved)
        self._disconnect_cid = self._chatroom.on_disconnect.subscribe(self.disconnect_recieved)
        self._chat_cid = self._chatroom.on_chat.subscribe(self.chat_recieved)
        userlist = [{"connection_id": connection_id, "nickname": connection_id, "is_asker": False} for connection_id in question.get_chatroom().get_connected_users()]
        message = {"type": "userlist", "data": userlist}
        self.write_message(json.dumps(message))

    def on_message(self, message):
        self._chatroom.add_chat(self._connection_id, message)

    def on_close(self):
        self._chatroom.on_connect.unsubscribe(self._connect_cid)
        self._chatroom.on_disconnect.unsubscribe(self._disconnect_cid)
        self._chatroom.on_chat.unsubscribe(self._chat_cid)
        self._chatroom.disconnect(self._connection_id)

    def connect_recieved(self, connected_id):
        message = {"type": "connect", "data": {"connection_id": connected_id, "nickname": connected_id, "is_asker": False}}
        self.write_message(json.dumps(message))

    def disconnect_recieved(self, disconnected_id):
        message = {"type": "disconnect", "data": {"connection_id": disconnected_id}}
        self.write_message(json.dumps(message))

    def chat_recieved(self, chat):
        sender_connection_id, text = chat
        message = {"type": "message", "data": {"connection_id": sender_connection_id, "message": text}}
        self.write_message(json.dumps(message))
