import unittest
from helpmio import event

class TestEvent(unittest.TestCase):

    def test_call(self):
        e = event.EventDispatcher()
        def callback(a, c, b):
            assert a == 1
            assert b == 2
            assert c == 3
        e.subscribe(callback)
        e(1, b=2, c=3)

    def test_unsubscribe(self):
        e = event.EventDispatcher()
        called = set()
        def callback1():
            called.add(1)
        def callback2():
            called.add(2)
        e.subscribe(callback1)
        e.subscribe(callback2)
        e.unsubscribe(callback1)
        e()
        assert 1 not in called
        assert 2 in called
