import os
import tornado.httpserver
import tornado.web

def init(port):
    template_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "..", "assets", "templates")
    app = tornado.web.Application([
        tornado.web.url(r"/", QuestionsHandler, name="main"),
    ], template_path=template_path, debug=True)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(port)


class QuestionsHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("questions.html")
