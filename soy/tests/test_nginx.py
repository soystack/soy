#!/usr/bin/env python

'''
Nose test for insuring quality assurance.
'''

from soy.nginx import Host
import nose
from nose.tools import raises, ok_
from mock import Mock, patch

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


def raise_(*args):
    '''
    raise lambda error
    '''
    raise OSError

class TestCreatePass:
    '''
    init
    '''
    def __init__(self):
        pass

    def setUp(self):
        '''
        set up
        '''
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
        inst = Host(self.__salt__, **self.vars)
        ret = inst.mkconf()
        ok_(ret == True, 'returned %s' % ret)

    def test_mksource_fail(self):
        inst = Host(self.__salt__, **self.vars)
        ret  = inst.mksource('/tmp/')
        ok_(ret == True, 'returned %s' % ret)

    def test_mkdir_pass(self):
        inst = Host(self.__salt__, **self.vars)
        ret = inst.mkdir('/tmp/')
        ok_(ret == True, 'returned %s' % ret)

    def test_mklog_pass(self):
        inst = Host(self.__salt__, **self.vars)
        ret = inst.mklog('/tmp/')
        ok_(ret == True, 'returned %s' % ret)

    def test_create_pass(self):
        inst = Host(self.__salt__, **self.vars)
        inst.mkconf = lambda: True
        inst.mkph = lambda x: True
        inst.mklog = lambda x: True
        ret = inst.create()
        ok_(ret == True, 'returned %s' % ret)

class TestCreateFail:
    '''
    init
    '''
    def __init__(self):
        pass

    def setUp(self):
        '''
        set up
        '''
        def raise_(e): raise OSError

        jinja = patch('jinja2.Template')
        jinja.return_value = raise_

        openfile = patch('__builtin__.open')
        openfile.return_value = raise_

        prepare = patch('soy.utils.prepare')
        prepare.return_value = raise_

        commit = patch('soy.utils.commit')
        prepare.return_value = raise_

        self.vars = {
            'user': 'user',
            'host': 'test.com'
        }

        self.__salt__ = {
            'pillar.raw': Pillar_raw,
            'file.remove': lambda x: raise_(Exception()),
            'file.symlink': lambda x, y: raise_(Exception()),
            'file.mkdir': lambda x: raise_(Exception()),
            'nginx.signal': lambda x: raise_(Exception())
        }

    def test_mkconf_fail(self):
        inst = Host(self.__salt__, **self.vars)
        ret  = inst.mkconf()
        ok_(ret == False, 'returned %s' % ret)

    @raises(OSError)
    def test_mksource_fail(self):
        inst = Host(self.__salt__, **self.vars)
        ret  = inst.mksource('/tmp/')

    def test_mkdir_fail(self):
        inst = Host(self.__salt__, **self.vars)
        ret = inst.mkdir('/tmp/')
        ok_(ret == False, 'returned %s' % ret)

    def test_mklog_fail(self):
        inst = Host(self.__salt__, **self.vars)
        ret = inst.mklog('/tmp/')
        ok_(ret == False, 'returned %s' % ret)

    def test_create_fail(self):
        def raise_(): raise OSError
        inst = Host(self.__salt__, **self.vars)
        inst.mkconf = lambda: raise_()
        inst.mkph = lambda x: raise_()
        inst.mklog = lambda x: raise_()
        ret = inst.create()
        ok_(ret == False, 'returned %s' % ret)

class TestDeleteFail:
    '''
    init
    '''
    def __init__(self):
        pass

    def setUp(self):
        '''
        set up
        '''

        jinja = patch('jinja2.Template')
        jinja.return_value = raise_
        openfile = patch('__builtin__.open')
        openfile.return_value = raise_
        prepare = patch('soy.utils.prepare')
        prepare.return_value = raise_
        commit = patch('soy.utils.commit')
        commit.return_value = raise_

        self.vars = {
            'user': 'user',
            'host': 'test.com'
        }

        self.__salt__ = {
            'pillar.raw': Pillar_raw,
            'file.remove': lambda x: raise_(),
            'file.symlink': lambda x, y: raise_(),
            'file.mkdir': lambda x: raise_(),
            'nginx.signal': lambda x: raise_()
        }

    def test_delete_fail(self):
        inst = Host(self.__salt__, **self.vars)
        ret  = inst.delete()
        ok_(ret == False, 'returned %s' % ret)

    def test_suspend_fail(self):
        inst = Host(self.__salt__, **self.vars)
        ret  = inst.suspend()
        ok_(ret == False, 'returned %s' % ret)

    def test_unsuspend_fail(self):
        inst = Host(self.__salt__, **self.vars)
        ret  = inst.unsuspend()
        ok_(ret == False, 'returned %s' % ret)

    def test_delete_user(self):
        inst = Host(self.__salt__, **self.vars)
        ret = inst.delete(user=True)
        ok_(ret == False, 'returned %s' % ret)

    def test_delete_enable(self):
        self.__salt__['file.remove'] = Mock(return_value=False)
        inst = Host(self.__salt__, **self.vars)
        ret = inst.delete()
        ok_(ret == False, 'returned %s' % ret)

class TestDeletePass:
    '''
    init
    '''
    def __init__(self):
        pass

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
        inst = Host(self.__salt__, **self.vars)
        ret  = inst.delete()
        ok_(ret == True, 'returned %s' % ret)

    def test_suspend_pass(self):
        inst = Host(self.__salt__, **self.vars)
        ret  = inst.suspend()
        ok_(ret == True, 'returned %s' % ret)

    def test_unsuspend_fail(self):
        inst = Host(self.__salt__, **self.vars)
        ret  = inst.unsuspend()
        ok_(ret == True, 'returned %s' % ret)

