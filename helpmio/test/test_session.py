import unittest
from helpmio import session

class TestSession(unittest.TestCase):

	def test_create(self):
		s = session.new_session()
		assert s != None

	def test_modify(self):
		s = session.new_session()
		s["123"] = 456
		assert s["123"] == 456

	def test_doesnt_exist(self):
		s = session.new_session()
		with self.assertRaises(KeyError):
			s["123"]

	def test_lookup(self):
		s1 = session.new_session()
		s2 = session.get_session(s1.get_sid())
		assert s1 == s2
