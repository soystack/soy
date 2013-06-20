#!/usr/bin/env python

'''
soy nginx function for rendering host configuration files.
'''

import nose
from nose.tools import raises, ok_
import soy.utils as soy
from mock import patch, Mock

def raise_(*args): raise OSError

class TestPrepareFail:
    def test_render_fail(self):
        ret = soy.prepare(None,'/fake/')
        ok_(ret == False, 'returned %s' % ret)

class TestPreparePass:
    def test_render_pass(self):
        ret = soy.prepare(None,'/tmp/test.file')
        ok_(ret == True, 'returned %s' % ret)
'''
class TestCommitFail:
    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.return_value = raise_

        soy.prepare = Mock(return_value=raise_)

    def test_commit_fail(self):
        ret = soy.commit('/tmp/', '/tmp/', **{})
        ok_(ret == False, 'returned %s' % ret)

class TestCommitPass:
    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.return_value = True

        soy.prepare = Mock(return_value=True)

    def test_commit_pass(self):
        ret = soy.commit('test.file', 'test.file', **{})
        ok_(ret == True, 'returned %s' % ret)
'''
