import uuid
import helpmio.event

class ChatRoom:

    def __init__(self):
        self._connected_users = dict()
        self._chat_history = []
        self.on_connect = helpmio.event.EventDispatcher()
        self.on_disconnect = helpmio.event.EventDispatcher()
        self.on_chat = helpmio.event.EventDispatcher()

    def connect(self, user):
        connection_id = str(uuid.uuid4())
        self._connected_users[connection_id] = user
        self.on_connect(connection_id)
        return connection_id

    def disconnect(self, connection_id):
        del self._connected_users[connection_id]
        self.on_disconnect(connection_id)

    def add_chat(self, connection_id, text):
        chat = (connection_id, text)
        self._chat_history.append(chat)
        self.on_chat(chat)

    def get_connected_users(self):
        return dict(self._connected_users)

    def get_chat_history(self):
        return self._chat_history[:]
