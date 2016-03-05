class EventDispatcher:

	def __init__(self):
		self._callbacks = set()

	def subscribe(self, callback):
		self._callbacks.add(callback)

	def unsubscribe(self, callback):
		self._callbacks.remove(callback)

	def __call__(self, *args, **kwargs):
		for callback in self._callbacks:
			callback(*args, **kwargs)
