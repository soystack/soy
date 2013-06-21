#!/usr/bin/env python

from soy.nginx import Host
import nose
from nose.tools import raises, ok_
from mock import Mock, patch, PropertyMock

Pillar_raw = lambda x: { 'enabled': '/tmp/',
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
                         'sushtdocs': '/var/www/suspended/htdocs/index.html' }

class TestCreatePass:

    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.return_value = True
        openfile = patch('__builtin__.open')
        openfile.return_value = True
        prepare = patch('soy.utils.prepare')
        prepare.return_value = True
        commit = patch('soy.utils.commit')
        commit.return_value = True

        self.vars = {
            'user': 'user',
            'host': 'test.com'
        }

        self.__salt__ = {
            'pillar.raw': Pillar_raw,
            'file.remove': lambda x: True,
            'file.symlink': lambda x, y: True,
            'file.mkdir': lambda x: True,
            'nginx.signal': lambda x: True
        }

    def test_mkconf_pass(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mkconf()
        ok_(rv == True, 'returned %s' % rv)

    def test_mksource_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mksource('/tmp/')
        ok_(rv == True, 'returned %s' % rv)

    def test_mkdir_pass(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mkdir('/tmp/')
        ok_(rv == True, 'returned %s' % rv)

    def test_mklog_pass(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mklog('/tmp/')
        ok_(rv == True, 'returned %s' % rv)

    def test_create_pass(self):
        t = Host(self.__salt__, **self.vars)
        t.mkconf = lambda: True
        t.mksource = lambda x: True
        t.mklog = lambda x: True
        rv = t.create()
        ok_(rv == True, 'returned %s' % rv)

class TestCreateFail:
    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.return_value = PropertyMock(side_effect=OSError)
        openfile = patch('__builtin__.open')
        openfile.return_value = PropertyMock(side_effect=OSError)
        prepare = patch('soy.utils.prepare')
        prepare.return_value = PropertyMock(side_effect=OSError)
        commit = patch('soy.utils.commit')
        prepare.return_value = PropertyMock(side_effect=OSError)

        self.vars = {
            'user': 'user',
            'host': 'test.com'
        }

        self.__salt__ = {
            'pillar.raw': Pillar_raw,
            'file.remove': lambda x: PropertyMock(side_effect=OSError),
            'file.symlink': lambda x, y: PropertyMock(side_effect=OSError),
            'file.mkdir': lambda x: PropertyMock(side_effect=OSError),
            'nginx.signal': lambda x: PropertyMock(side_effect=OSError)
        }

    def test_mkconf_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mkconf()
        ok_(rv == False, 'returned %s' % rv)

    @raises(OSError)
    def test_mksource_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mksource('/tmp/')

    def test_mkdir_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mkdir('/tmp/')
        ok_(rv == False, 'returned %s' % rv)

    def test_mklog_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.mklog('/tmp/')
        ok_(rv == False, 'returned %s' % rv)

    def test_create_fail(self):
        t = Host(self.__salt__, **self.vars)
        t.mkconf = lambda: PropertyMock(side_effect=OSError)
        t.mksource = lambda x: PropertyMock(side_effect=OSError)
        t.mklog = lambda x: PropertyMock(side_effect=OSError)
        rv = t.create()
        ok_(rv == False, 'returned %s' % rv)

class TestDeleteFail:

    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.return_value = PropertyMock(side_effect=OSError)
        openfile = patch('__builtin__.open')
        openfile.return_value = PropertyMock(side_effect=OSError)
        prepare = patch('soy.utils.prepare')
        prepare.return_value = PropertyMock(side_effect=OSError)
        commit = patch('soy.utils.commit')
        commit.return_value = PropertyMock(side_effect=OSError)

        self.vars = {
            'user': 'user',
            'host': 'test.com'
        }

        self.__salt__ = {
            'pillar.raw': Pillar_raw,
            'file.remove': lambda x: PropertyMock(side_effect=OSError),
            'file.symlink': lambda x, y: PropertyMock(side_effect=OSError),
            'file.mkdir': lambda x: PropertyMock(side_effect=OSError),
            'nginx.signal': lambda x: PropertyMock(side_effect=OSError)
        }

    def test_delete_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv  = t.delete()
        ok_(rv == False, 'returned %s' % rv)

    def test_suspend_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv  = t.suspend()
        ok_(rv == False, 'returned %s' % rv)

    def test_unsuspend_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv  = t.unsuspend()
        ok_(rv == False, 'returned %s' % rv)

    def test_delete_user(self):
        t = Host(self.__salt__, **self.vars)
        rv = t.delete(user=True)
        ok_(rv == False, 'returned %s' % rv)

class TestDeletePass:

    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.return_value = True
        openfile = patch('__builtin__.open')
        openfile.return_value = True
        prepare = patch('soy.utils.prepare')
        prepare.return_value = True
        commit = patch('soy.utils.commit')
        commit.return_value = True
        
        self.vars = {
            'user': 'user',
            'host': 'test.com'
        }
        self.__salt__ = {
            'pillar.raw': Pillar_raw,
            'file.remove': lambda x: True,
            'file.symlink': lambda x, y: True,
            'file.mkdir': lambda x: True,
            'nginx.signal': lambda x: True
        }

    def test_delete_pass(self):
        t = Host(self.__salt__, **self.vars)
        rv  = t.delete()
        ok_(rv == True, 'returned %s' % rv)

    def test_suspend_pass(self):
        t = Host(self.__salt__, **self.vars)
        rv  = t.suspend()
        ok_(rv == True, 'returned %s' % rv)

    def test_unsuspend_fail(self):
        t = Host(self.__salt__, **self.vars)
        rv  = t.unsuspend()
        ok_(rv == True, 'returned %s' % rv)
