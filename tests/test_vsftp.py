#!/use/bin/env python

import nose
from soy.vsftp import User
from nose.tools import raises, ok_ 
from mock import Mock, patch, MagicMock

class Start:
	def __init__(self):
		self.salt = {'cmd.run': lambda *x: True,
					 'file.remove': lambda*x: True}

@patch('bsddb.db.DB')
class TestUserPass(Start):
	def test_report(self, DB):
		t = User(self.salt, **{}).report()
		ok_('status' not in t, 't is %s' % t)

	def test_create(self, DB):
		t = User(self.salt, **{}).create()
		ok_(t['status'] is True, 't is %s' % t)

	def test_delete(self, DB):
		t = User(self.salt, **{}).delete()
		ok_(t['status'] is True, 't is %s' % t)
	
	def test_update(self, DB):
		t = User(self.salt, **{}).update()
		ok_(t['status'] is True, 't is %s' % t)


@patch('bsddb.db.DB', new_callable=OSError)
class TestUserFail(Start):
	def test_report(self, DB):
		t = User(self.salt, **{}).report()
		ok_(t['status'] is False, 't is %s' % t)

	def test_create(self, DB):
		t = User(self.salt, **{}).create()
		ok_(t['status'] is False, 't is %s' % t)
	
	def test_delete(self, DB):
		t = User(self.salt, **{}).delete()
		ok_(t['status'] is False, 't is %s' % t)

	def test_update(self, DB):
		t = User(self.salt, **{}).update()
		ok_(t['status'] is False, 't is %s' % t)

