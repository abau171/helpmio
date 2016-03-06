import uuid
import helpmio.chat


class Question:

    def __init__(self, asker_name, title, description, tags):
        self._qid = str(uuid.uuid4())
        self._title = title
        self._description = description
        self._tags = [tag.lower() for tag in tags]
        self._is_resolved = False
        self._chatroom = helpmio.chat.ChatRoom(asker_name)

    def get_qid(self):
        return self._qid

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_truncated_description(self):
        max_chars = 250
        if len(self._description) > max_chars:
            return (self._description[:max_chars] + '...')
        else:
            return self._description

    def get_is_resolved(self):
        return self._is_resolved

    def get_chatroom(self):
        return self._chatroom

    def get_tags(self):
        return self._tags[:]

    def has_tag(self, tag):
        return tag.lower() in self._tags

    def set_resolved(self):
        self._is_resolved = True


class _QuestionManager:

    def __init__(self):
        self._questions = dict()

    def new_question(self, asker, title, description, tags):
        question = Question(asker, title, description, tags)
        self._questions[question.get_qid()] = question
        return question

    def get_question(self, qid):
        if qid in self._questions:
            return self._questions[qid]
        else:
            return None

    def get_all_questions(self):
        return list(self._questions.values())

    def filter_questions(self, is_resolved, tag):
        return [question for question in self._questions.values()
                if (is_resolved == None or question.get_is_resolved() == is_resolved)
                and (tag == None or question.has_tag(tag))
                ]


_question_manager = _QuestionManager()


def new_question(asker, title, description, tags):
    return _question_manager.new_question(asker, title, description, tags)


def get_question(qid):
    return _question_manager.get_question(qid)


def get_all_questions():
    return _question_manager.get_all_questions()


def filter_questions(is_resolved=None, tag=None):
    return _question_manager.filter_questions(is_resolved, tag)
