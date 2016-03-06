import uuid
import helpmio.chat


class Question:

    def __init__(self, title, description):
        self._qid = str(uuid.uuid4())
        self._title = title
        self._description = description
        self._is_resolved = False
        self._chatroom = helpmio.chat.ChatRoom()

    def get_qid(self):
        return self._qid

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_is_resolved(self):
        return self._chatroom

    def get_chatroom(self):
        return self._chatroom

    def set_resolved(self):
        self._is_resolved = True


class _QuestionManager:

    def __init__(self):
        self._questions = dict()

    def new_question(self, title, description):
        question = Question(title, description)
        self._questions[question.get_qid()] = question
        return question

    def get_question(self, qid):
        if qid in self._questions:
            return self._questions[qid]
        else:
            return None


_question_manager = _QuestionManager()


def new_question(title, description):
    return _question_manager.new_question(title, description)


def get_question(qid):
    return _question_manager.get_question(qid)
