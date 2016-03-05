import chat
import session

room = chat.ChatRoom()

a = session.new_session()
a["nickname"] = "A"
b = session.new_session()
b["nickname"] = "B"

def session_connect(session):
	print("SESSION CONNECTED:", session)

def session_disconnect(session):
	print("SESSION DISCONNECTED:", session)

def chatted(chat):
	nickname, text = chat
	print("{}: {}".format(nickname, text))

room.on_session_connect.subscribe(session_connect)
room.on_session_disconnect.subscribe(session_disconnect)
room.on_chat.subscribe(chatted)

room.connect_session(a)
room.connect_session(b)
room.add_chat(a, "HELLO")
room.add_chat(b, "HELLO THERE")
room.disconnect_session(b)
room.disconnect_session(a)
