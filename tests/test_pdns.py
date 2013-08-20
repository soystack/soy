#!/usr/bin/env python

import nose
from soy.pdns import DNS, Domain, Record
from nose.tools import raises, ok_
from mock import Mock, patch, MagicMock

def raise_(*x):
	raise Exception

class Start:
	def start(self, p=None):
		def pillar_raw(p):
			if p == 'pdns-master':
				return {'db': 'test'}
			return 'test'

		self.__salt__ = {'pillar.raw': pillar_raw}

@patch('MySQLdb.connect')
class TestDNSPass(Start):
	def setUp(self):
		self.start()

	def test_dbconnect(self, connect):
		t = DNS(self.__salt__, **{}).dbconnect()
		ok_(t['status'] is True, 'returned %s' % t['status'])

@patch('MySQLdb.connect')
class TestDomainPass(Start):
	def setUp(self):
		self.start()

	def test_create(self, connect):
		t = Domain(self.__salt__, **{}).create()
		ok_(t['status'] is True, 'returned %s' % t['status'])

	def test_report(self, connect):
		t = Domain(self.__salt__, **{}).report()
		ok_('status' not in t, 'returned %s' % t.get('status', 'error'))
	
	def test_search(self, connect):
		t = Domain(self.__salt__, **{}).search()
		ok_('status' not in t, 'returned %s' % t.get('status', 'error'))

	def test_update_diff(self, connect):
		t = MagicMock()
		t = Domain(self.__salt__, **{}).update_diff(bytearray(7))
		ok_('status' not in t, 'returned %s' % t.get('status', 'error'))

	def test_update(self, connect):
		t = Domain(self.__salt__, **{}).update()
		ok_(t['status'] is True, 'returned %s' % t['status'])

	def test_delete(self, connect):
		t = Domain(self.__salt__, **{}).delete()
		ok_(t['status'] is True, 'returned %s' % t['status'])

@patch('MySQLdb.connect')
class TestRecordPass(Start):
	def setUp(self):
		self.start()

	def test_create(self, connect):
		t = Record(self.__salt__, **{}).create()
		ok_(t['status'] is True, 'returned %s' % t['status'])

	def test_report(self, connect):
		t = Record(self.__salt__, **{}).report()
		ok_('status' not in t, 'returned %s' % t.get('status', 'error'))
	
	def test_search(self, connect):
		t = Record(self.__salt__, **{}).search()
		ok_('status' not in t, 'returned %s' % t.get('status', 'error'))

	def test_update_diff(self, connect):
		t = MagicMock()
		t = Record(self.__salt__, **{}).update_diff(bytearray(10))
		ok_('status' not in t, 'returned %s' % t.get('status', 'error'))

	def test_update(self, connect):
		t = Record(self.__salt__, **{}).update()
		ok_(t['status'] is True, 'returned %s' % t['status'])

	def test_delete(self, connect):
		t = Record(self.__salt__, **{}).delete()
		ok_(t['status'] is True, 'returned %s' % t['status'])

@patch('MySQLdb.connect', new_callable=OSError)
class TestDomainFail(Start):
	def setUp(self):
		self.start()

	def test_create(self, connect):
		t = Domain(self.__salt__, **{}).create()
		ok_(t['status'] is False, 'returned %s' % t['status'])

	def test_report(self, connect):
		t = Domain(self.__salt__, **{}).report()
		ok_('status' in t, 'returned %s' % t.get('status', 'error'))
	
	def test_search(self, connect):
		t = Domain(self.__salt__, **{}).search()
		ok_('status' in t, 'returned %s' % t.get('status', 'error'))

	@patch('__builtin__.hasattr', return_value=raise_)
	def test_update_diff(self, connect, ignore):
		t = MagicMock()
		for attr in dir(t): del attr
		t = Domain(self.__salt__, **{}).update_diff(bytearray(7))
		ok_('status' in t, 'returned %s' % t.get('status', 'error'))

	def test_update(self, connect):
		t = Domain(self.__salt__, **{}).update()
		ok_(t['status'] is False, 'returned %s' % t['status'])

	def test_delete(self, connect):
		t = Domain(self.__salt__, **{}).delete()
		ok_(t['status'] is False, 'returned %s' % t['status'])

@patch('MySQLdb.connect', new_callable=OSError)
class TestRecordFail(Start):
	def setUp(self):
		self.start(patch('MySQLdb.connect', new_callable=OSError))

	def test_create(self, connect):
		t = Record(self.__salt__, **{}).create()
		ok_(t['status'] is False, 'returned %s' % t['status'])

	def test_report(self, connect):
		t = Record(self.__salt__, **{}).report()
		ok_('status' in t, 'returned %s' % t.get('status', 'error'))
	
	def test_search(self, connect):
		t = Record(self.__salt__, **{}).search()
		ok_('status' in t, 'returned %s' % t.get('status', 'error'))

	@patch('__builtin__.hasattr', return_value=raise_)
	def test_update_diff(self, connect, ignore):
		t = MagicMock()
		t = Record(self.__salt__, **{}).update_diff(bytearray(10))
		ok_('status' in t, 'returned %s' % t.get('status', 'error'))

	def test_update(self, connect):
		t = Record(self.__salt__, **{}).update()
		ok_(t['status'] is False, 'returned %s' % t['status'])

	def test_delete(self, connect):
		t = Record(self.__salt__, **{}).delete()
		ok_(t['status'] is False, 'returned %s' % t['status'])

