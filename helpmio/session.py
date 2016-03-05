import uuid


class Session:

    def __init__(self):
        self._sid = str(uuid.uuid4())
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
        if sid in self.sessions:
            return self.sessions[sid]
        else:
            return None


_sessionManager = _SessionManager()


def new_session():
    return _sessionManager.new_session()


def get_session(sid):
    return _sessionManager.get_session(sid)
