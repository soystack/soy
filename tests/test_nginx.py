#!/usr/bin/env python

import nose
from nose.tools import raises, ok_
from mock import Mock, patch

import sys
sys.path.append('../salt/modules')
import soy_nginx

class Start:
    def start(self, case):
        Pillar_raw = { 'nginx': {'enabled': '/tmp/',
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
                                 'sushtdocs': '/var/www/suspended/htdocs/index.html'}}

        jinja = patch('jinja2.Template')
        jinja.return_value = case
        openfile = patch('__builtin__.open')
        openfile.return_value = case
        prepare = patch('soy_utils.prepare')
        prepare.return_value = case
        commit = patch('soy_utils.commit')
        commit.return_value = case
        listdir = patch('os.listdir')
        listdir.return_value = ['t','e','s','t']

        self.vars = {
            'user': 'user',
            'host': 'test.com'
        }

        soy_nginx.__pillar__ = Pillar_raw

        soy_nginx.__salt__ = {
            'pillar.raw': Pillar_raw,
            'file.remove':  case,
            'file.symlink': case,
            'file.mkdir':   case,
            'file.rename': case,
            'nginx.signal': case,
            'soy_utils.commit': case,
            'soy_utils.prepare': case
        }


class TestCreatePass(Start):
    def setUp(self):
        self.start(lambda *x, **y: True)

    def test_mkconf_pass(self):
        rv = soy_nginx._mkconf(**self.vars)
        ok_(rv is True, 'returned %s' % rv)

    def test_mksource_pass(self):
        rv = soy_nginx._mksource('/htdocs', **self.vars)
        ok_(rv is True, 'returned %s' % rv)

    def test_mkdir_pass(self):
        rv = soy_nginx._mkdir('/htdocs', **self.vars)
        ok_(rv is True, 'returned %s' % rv)

    def test_mklog_pass(self):
        rv = soy_nginx._mklog('/log')
        ok_(rv is True, 'returned %s' % rv)
        
    def test_update_pass(self):
        rv = soy_nginx.update('user', 'host', 'updated_host')
        ok_(rv['status'] is True, 'returned %s' % rv)
    
    @patch('os.listdir')
    def test_report_pass(self, p):
        p.return_value = ['t','e','s','t']
        rv = soy_nginx.report('user')
        ok_(rv is not False, 'returned %s' % rv)

    def test_create_pass(self):
        soy_nginx._mkconf = lambda **x: True
        soy_nginx._mkdir = lambda x, **y: True
        soy_nginx._mklog = lambda x: True
        rv = soy_nginx.create('user', 'host')
        ok_(rv is True, 'returned %s' % rv)


class TestCreateFail(Start):
    def setUp(self):
        self.start(Mock(side_effect=OSError))

    @raises(OSError)
    def test_mkconf_fail(self):
        rv = soy_nginx._mkconf(**self.vars)
        ok_(rv is False, 'returned %s' % rv)

    @raises(OSError)
    def test_mksource_fail(self):
        rv = soy_nginx._mksource('/htdocs', **self.vars)

    @raises(OSError)
    def test_mkdir_fail(self):
        rv = soy_nginx._mkdir('/htdocs', **self.vars)
        ok_(rv is False, 'returned %s' % rv)

    @raises(OSError)
    def test_mklog_fail(self):
        rv = soy_nginx._mklog('/log')
        ok_(rv is False, 'returned %s' % rv)

    def test_update_fail(self):
        rv = soy_nginx.update('user', 'host', 'updated_user')
        ok_(rv['status'] is False, 'returned %s' % rv)

    @patch('os.listdir')
    def test_report_fail(self, p):
        p.return_value = ['t','e','s','t']
        rv = soy_nginx.report('user')
        ok_(rv is not True, 'returned %s' % rv)

    def test_create_fail(self):
        soy_nginx._mkconf = Mock(side_effect=OSError)
        soy_nginx._mkdir = Mock(side_effect=OSError)
        soy_nginx._mklog = Mock(side_effect=OSError)
        rv = soy_nginx.create('user', 'host')
        ok_(rv is False, 'returned %s' % rv)


class TestDeleteFail(Start):

    def setUp(self):
        self.start(Mock(side_effect=OSError))

    def test_delete_fail(self):
        rv = soy_nginx.delete('user', 'host')
        ok_(rv is False, 'returned %s' % rv)

    def test_suspend_fail(self):
        rv = soy_nginx.suspend(**self.vars)
        ok_(rv is False, 'returned %s' % rv)

    def test_unsuspend_fail(self):
        rv = soy_nginx.unsuspend(**self.vars)
        ok_(rv is False, 'returned %s' % rv)


class TestDeleteTrue(Start):

    def setUp(self):
        self.start(lambda *x, **y: True)

    def test_delete_true(self):
        rv = soy_nginx.delete('user', 'host')
        ok_(rv is True, 'returned %s' % rv)

    def test_suspend_true(self):
        rv = soy_nginx.suspend(**self.vars)
        ok_(rv is True, 'returned %s' % rv)

    def test_unsuspend_true(self):
        rv = soy_nginx.unsuspend(**self.vars)
        ok_(rv is True, 'returned %s' % rv)
