import uuid
import helpmio.chat


class Question:

    def __init__(self, title, description, tags):
        self._qid = str(uuid.uuid4())
        self._title = title
        self._description = description
        self._tags = tags
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

    def get_tags(self):
        return self._tags[:]

    def has_tag(self, tag):
        return tag in self._tags

    def set_resolved(self):
        self._is_resolved = True


class _QuestionManager:

    def __init__(self):
        self._questions = dict()

    def new_question(self, title, description, tags):
        question = Question(title, description, tags)
        self._questions[question.get_qid()] = question
        return question

    def get_question(self, qid):
        if qid in self._questions:
            return self._questions[qid]
        else:
            return None

    def get_all_questions(self):
        return list(self._questions.values())

    def get_questions_by_tag(self, tag):
        return [question for question in self._questions.values() if question.has_tag(tag)]


_question_manager = _QuestionManager()


def new_question(title, description, tags):
    return _question_manager.new_question(title, description, tags)


def get_question(qid):
    return _question_manager.get_question(qid)


def get_all_questions():
    return _question_manager.get_all_questions()


def get_questions_by_tag(tag):
    return _question_manager.get_questions_by_tag(tag)
