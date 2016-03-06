import helpmio.question
import helpmio.session
import os
import tornado.httpserver
import tornado.web
import tornado.websocket
import json
import re

def init(port):
    template_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "assets", "templates")
    static_files_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "assets", "web")
    favicon_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "assets")
    app = tornado.web.Application([
        tornado.web.url(r"/", MainHandler, name="main"),
        tornado.web.url(r"/login", LoginHandler, name="login"),
        tornado.web.url(r"/questions/new", NewQuestionHandler, name="new_question"),
        tornado.web.url(r"/questions/(.*)", QuestionHandler, name="question"),
        tornado.web.url(r"/ws/(.*)", QuestionWebSocketHandler, name="question_websocket"),
        tornado.web.url(r"/assets/(.*)", tornado.web.StaticFileHandler, {"path": static_files_path}, name="static"),
        tornado.web.url(r"/(favicon\.ico)", tornado.web.StaticFileHandler, {"path": favicon_path}, name="favicon")
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


class BaseHandler(tornado.web.RequestHandler):

    def get_template_namespace(self):
        namespace = super(BaseHandler, self).get_template_namespace()
        namespace["session"] = self.session
        return namespace


class MainHandler(BaseHandler):

    @_inject_sessions
    def get(self):
        tag = self.get_argument("tag", default=None)
        questions = helpmio.question.filter_questions(is_resolved=False, tag=tag)
        self.render("question_list.html", questions=questions)


class LoginHandler(BaseHandler):

    @_inject_sessions
    def get(self):
        if self.get_query_argument("lo", "") == "1":
            del self.session["logged_in"]
            del self.session["nickname"]
            self.redirect(self.reverse_url("main"))
            return
        error = None
        if self.get_query_argument("error", "") == "1":
            error = "Username cannot be empty."
        self.render("login.html", error=error)

    @_inject_sessions
    def post(self):
        username = self.get_body_argument("username")
        if username == "":
            self.redirect(self.reverse_url("login") + "?error=1")
            return
        self.session["logged_in"] = True
        self.session["nickname"] = username
        self.redirect(self.reverse_url("main"))


class NewQuestionHandler(BaseHandler):

    @_inject_sessions
    def get(self):
        error = None
        error_arg = self.get_query_argument("error", "")
        if error_arg == "1":
            error = "Fields cannot be empty."
        self.render("new_question.html", error=error)

    @_inject_sessions
    def post(self):
        title = self.get_body_argument("title")
        description = self.get_body_argument("description")
        if title == "" or description == "":
            self.redirect(self.reverse_url("new_question") + "?error=1")
            return
        self.redirect(self.reverse_url("question",
            helpmio.question.new_question(
                title, description, re.split(r"[, ]+", self.get_body_argument("tags"))).get_qid()))


class QuestionHandler(BaseHandler):

    @_inject_sessions
    def get(self, qid):
        self.render("question.html", qid=qid)


class QuestionWebSocketHandler(tornado.websocket.WebSocketHandler):
    
    @_inject_sessions
    def open(self, qid):
        self._nickname = self.session["nickname"]
        question = helpmio.question.get_question(qid)
        self._chatroom = question.get_chatroom()
        self._connection_id = self._chatroom.connect(self._nickname)
        self._connect_cid = self._chatroom.on_connect.subscribe(self.connect_recieved)
        self._disconnect_cid = self._chatroom.on_disconnect.subscribe(self.disconnect_recieved)
        self._chat_cid = self._chatroom.on_chat.subscribe(self.chat_recieved)
        userlist = [{"connection_id": connection_id,
                     "nickname": nickname,
                     "is_asker": False}
                     for connection_id, nickname in self._chatroom.get_all_users().items()]
        onlinelist = [connection_id for connection_id in self._chatroom.get_connected_users().values()]
        chat_history = self._chatroom.get_chat_history()
        message = {"type": "curstate", "data": {"userlist": userlist, "onlinelist": onlinelist, "history": chat_history}}
        self.write_message(json.dumps(message))

    def on_message(self, message):
        message_obj = json.loads(message)
        message_type = message_obj["type"]
        data = message_obj["data"]
        if message_type == "message":
            if self._nickname != None:
                self._chatroom.add_chat(self._connection_id, data)
            else:
                print("user cannot send message without nickname")
        else:
            print("invalid client message type: '{}'".format(message_type))

    def on_close(self):
        self._chatroom.on_connect.unsubscribe(self._connect_cid)
        self._chatroom.on_disconnect.unsubscribe(self._disconnect_cid)
        self._chatroom.on_chat.unsubscribe(self._chat_cid)
        self._chatroom.disconnect(self._connection_id)

    def connect_recieved(self, connected_id):
        nickname = self._chatroom.get_user(connected_id)
        message = {"type": "connect", "data": {"connection_id": connected_id, "nickname": nickname, "is_asker": False}}
        self.write_message(json.dumps(message))

    def disconnect_recieved(self, disconnected_id):
        message = {"type": "disconnect", "data": {"connection_id": disconnected_id}}
        self.write_message(json.dumps(message))

    def chat_recieved(self, chat):
        sender_connection_id, text = chat
        nickname = self._chatroom.get_user(sender_connection_id)
        if nickname != None:
            message = {"type": "message", "data": {"connection_id": sender_connection_id, "message": text}}
            self.write_message(json.dumps(message))
