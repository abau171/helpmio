import uuid


class _Session:

    def __init__(self):
        self._sid = uuid.uuid4()
        self._data = dict()

    def getSid(self):
        return self._sid

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value


class _SessionManager:

    def __init__(self):
        self.sessions = dict()

    def newSession(self):
        session = _Session()
        self.sessions[session.getSid()] = session
        return session

    def getSession(self, sid):
        return self.sessions[sid]


_sessionManager = _SessionManager()

def getSession(sid):
    if sid == None:
        return _sessionManager.newSession()
    else:
        return _sessionManager.getSession(sid)
