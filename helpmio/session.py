import uuid


class Session:

    def __init__(self):
        self._sid = str(uuid.uuid4())
        self._data = dict()
        self["watched"] = set()

    def get_sid(self):
        return self._sid

    def __getitem__(self, key):
        if key in self._data:
            return self._data[key]
        else:
            return None

    def __setitem__(self, key, value):
        self._data[key] = value

    def __delitem__(self, key):
        del self._data[key]

    def __contains__(self, key):
        return key in self._data

    def __missing__(self, key):
        return key not in self._data


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


_session_manager = _SessionManager()


def new_session():
    return _session_manager.new_session()


def get_session(sid):
    return _session_manager.get_session(sid)
