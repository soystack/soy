#!/use/bin/env python

import nose
from soy.vsftp import User
from nose.tools import raises, ok_ 
from mock import Mock, patch, MagicMock

@patch('bsddb.db.DB')
class TestUserPass:
	def test_report(self, DB):
		t = User(**{}).report()
		ok_('status' not in t, 't is %s' % t)

	def test_create(self, DB):
		t = User(**{}).create()
		ok_(t['status'] is True, 't is %s' % t)

@patch('bsddb.db.DB', new_callable=OSError)
class TestUserFail:
	def test_report(self, DB):
		t = User(**{}).report()
		ok_('status' in t, 't is %s' % t)

	def test_create(self, DB):
		t = User(**{}).create()
		ok_(t['status'] is False, 't is %s' % t)
