#!/usr/bin/env python

import nose
from soy.nginx import Host
from nose.tools import raises, ok_
from mock import Mock, patch



class Start:
    def start(self, case):
        Pillar_raw = lambda x: {'enabled': '/tmp/',
                                'available': '/tmp/',
                                'base': '/tmp/',
                                'template': '/tmp/test.file',
                                'index': '/tmp/test.file',
                                'indexhtml': 'test.html',
                                'access': 'access.test',
                                'error': 'error.test',
                                'htdocs': '/tmp/',
                                'logs': '/tmp/',
                                'susconf': '/etc/nginx/suspended.conf.tpl',
                                'sushtml': '/etc/nginx/suspended.html.tpl',
                                'sushtdocs': '/var/www/suspended/htdocs/index.html'}

        jinja = patch('jinja2.Template')
        jinja.return_value = case
        openfile = patch('__builtin__.open')
        openfile.return_value = case
        prepare = patch('soy.utils.prepare')
        prepare.return_value = case
        commit = patch('soy.utils.commit')
        commit.return_value = case

        self.vars = {
            'user': 'user',
            'host': 'test.com'
        }

        self.__salt__ = {
            'pillar.raw': Pillar_raw,
            'file.remove':  case,
            'file.symlink': case,
            'file.mkdir':   case,
            'nginx.signal': case
        }


class TestCreatePass(Start):
    def setUp(self):
        self.start(lambda *x: True)

    def test_mkconf_pass(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mkconf()
        ok_(rv is True, 'returned %s' % rv)

    def test_mksource_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mksource('/tmp/')
        ok_(rv is True, 'returned %s' % rv)

    def test_mkdir_pass(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mkdir('/tmp/')
        ok_(rv is True, 'returned %s' % rv)

    def test_mklog_pass(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mklog('/tmp/')
        ok_(rv is True, 'returned %s' % rv)
        
	def test_update_pass(self):
		t = Host(self.__salt__, **self.vars)
		rv = t.update()
		ok_(rv is True, 'returned %s' % rv)
		
	def test_report_pass(self):
		t = Host(self.__salt__, **self.vars)
		rv = t.report()
		ok_(rv is True, 'returned %s' % rv)

    def test_create_pass(self):
        t = Host(self.__salt__, **self.vars)
        t.mkconf = lambda: True
        t.mkdir = lambda x: True
        t.mklog = lambda x: True
        rv = t.create()
        ok_(rv is True, 'returned %s' % rv)


class TestCreateFail(Start):
    def setUp(self):
        self.start(Mock(side_effect=OSError))

    def test_mkconf_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mkconf()
        ok_(rv is False, 'returned %s' % rv)

    @raises(OSError)
    def test_mksource_fail(self):
        t = Host(self.__salt__, **self.vars)
        t.mksource('/tmp/')

    def test_mkdir_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mkdir('/tmp/')
        ok_(rv is False, 'returned %s' % rv)

    def test_mklog_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mklog('/tmp/')
        ok_(rv is False, 'returned %s' % rv)

	def test_update_fail(self):
		t = Host(self.__salt__, **self.vars)
		rv = t.update()
		ok_(rv is False, 'returned %s' % rv)

	def test_report_fail(self):
		t = Host(self.__salt__, ** self.vars)
		rv = t.report()
		ok_(rv is False, 'returned %s' % rv)

    def test_create_fail(self):
        t = Host(self.__salt__, **self.vars)
        t.mkconf = Mock(side_effect=OSError)
        t.mkdir = Mock(side_effect=OSError)
        t.mklog = Mock(side_effect=OSError)
        rv = t.create()
        ok_(rv is False, 'returned %s' % rv)


class TestDeleteFail(Start):

    def setUp(self):
        self.start(Mock(side_effect=OSError))

    def test_delete_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.delete()
        ok_(rv is False, 'returned %s' % rv)

    def test_suspend_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.suspend()
        ok_(rv is False, 'returned %s' % rv)

    def test_unsuspend_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.unsuspend()
        ok_(rv is False, 'returned %s' % rv)

    def test_delete_user(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.delete(user=True)
        ok_(rv is False, 'returned %s' % rv)


class TestDeleteTrue(Start):

    def setUp(self):
        self.start(lambda *x: True)

    def test_delete_true(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.delete()
        ok_(rv is True, 'returned %s' % rv)

    def test_suspend_true(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.suspend()
        ok_(rv is True, 'returned %s' % rv)

    def test_unsuspend_true(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.unsuspend()
        ok_(rv is True, 'returned %s' % rv)
