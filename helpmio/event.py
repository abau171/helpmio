import helpmio.id_gen

class EventDispatcher:

    def __init__(self):
        self._cid_gen = helpmio.id_gen.IdGenerator()
        self._callbacks = dict()

    def subscribe(self, callback):
        cid = self._cid_gen.gen_id()
        self._callbacks[cid] = callback
        return cid

    def unsubscribe(self, cid):
        del self._callbacks[cid]

    def __call__(self, *args, **kwargs):
        for callback in self._callbacks.values():
            callback(*args, **kwargs)
