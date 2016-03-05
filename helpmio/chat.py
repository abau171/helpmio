import event

class ChatRoom:

	def __init__(self):
		self._online_sessions = set()
		self._chats = []
		self.on_session_connect = event.EventDispatcher()
		self.on_session_disconnect = event.EventDispatcher()
		self.on_chat = event.EventDispatcher()

	def connect_session(self, session):
		self._online_sessions.add(session)
		self.on_session_connect(session)

	def disconnect_session(self, session):
		self._online_sessions.remove(session)
		self.on_session_disconnect(session)

	def get__online_sessions(self):
		return self._online_sessions

	def add_chat(self, session, text):
		chat = (session["nickname"], text)
		self._chats.append(chat)
		self.on_chat(chat)

	def get_chat(self, i):
		return self._chats[i]

	def get_all_chats(self):
		return self._chats
