#!/usr/bin/env python

'''
soy nginx function for rendering host configuration files.
'''

import nose
from nose.tools import raises, ok_
import soy.utils as soy
from mock import patch, MagicMock

def raise_(*args): raise OSError

class TestPrepareFail:
    def test_render_fail(self):
        ret = soy.prepare(None,'/fakedir/')
        ok_(ret == False, 'returned %s' % ret)

class TestPreparePass:
    def test_render_pass(self):
        ret = soy.prepare(None,'/tmp/test.file')
        ok_(ret == True, 'returned %s' % ret)

class TestCommitFail:
    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.return_value = raise_

        openfile = patch('__builtin__.open')
        openfile.return_value = raise_

        render = patch('soy.utils.prepare')
        render.return_value = raise_

    def test_render_fail(self):
        ret = soy.commit('/tmp/', '/tmp/', **{})
        ok_(ret == False, 'returned %s' % ret)

class TestCommitPass:
    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.return_value = True

        openfile = patch('__builtin__.open')
        openfile.return_value = True

        render = patch('soy.utils.prepare')
        render.return_value = True

    def test_commit_pass(self):
        ret = soy.commit('/etc/nginx/virtualhost.conf.tpl', '/tmp/', **{})
        ok_(ret == False, 'returned %s' % ret)
