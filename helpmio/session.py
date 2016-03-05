import uuid


class Session:

    def __init__(self):
        self._sid = uuid.uuid4()
        self._data = dict()

    def get_sid(self):
        return self._sid

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value


class _SessionManager:

    def __init__(self):
        self.sessions = dict()

    def new_session(self):
        session = Session()
        self.sessions[session.get_sid()] = session
        return session

    def get_session(self, sid):
        return self.sessions[sid]


_sessionManager = _SessionManager()


def get_session(sid):
    if sid == None:
        return _sessionManager.new_session()
    else:
        return _sessionManager.get_session(sid)
