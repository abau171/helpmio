import uuid
import helpmio.event


class ChatRoom:

    def __init__(self, asker_name):
        self._connected_users = dict()
        self._all_users = dict()
        self._chat_history = []
        self.on_connect = helpmio.event.EventDispatcher()
        self.on_disconnect = helpmio.event.EventDispatcher()
        self.on_chat = helpmio.event.EventDispatcher()
        self._asker_name = asker_name

    def connect(self, nickname):
        connection_id = str(uuid.uuid4())
        self._connected_users[connection_id] = nickname
        self._all_users[connection_id] = nickname
        self.on_connect(connection_id)
        return connection_id

    def disconnect(self, connection_id):
        del self._connected_users[connection_id]
        self.on_disconnect(connection_id)

    def add_chat(self, connection_id, text):
        chat = (connection_id, text)
        self._chat_history.append(chat)
        self.on_chat(chat)

    def get_user(self, connection_id):
        return self._all_users[connection_id]

    def get_connected_users(self):
        return dict(self._connected_users)

    def get_num_connected_users(self):
        return len(self._connected_users)

    def get_all_users(self):
        return dict(self._all_users)

    def get_chat_history(self):
        return self._chat_history[:]

    def get_asker_name(self):
        return self._asker_name

    def asker_is_connected(self):
        for nickname in self._connected_users.values():
            if nickname == self._asker_name:
                return True
        return False

    def non_asker_is_connected(self):
        for nickname in self._connected_users.values():
            if nickname != self._asker_name:
                return True
        return False
