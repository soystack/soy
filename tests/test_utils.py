#!/usr/bin/env python

import soy.utils as soy
from nose.tools import ok_
from mock import patch, Mock


class TestPrepareTrue:
    def test_true(self):
        rv = soy.prepare(None, '/fake/')
        ok_(rv is False, 'returned %s' % rv)


class TestPrepareFalse:
    def test_pass(self):
        rv = soy.prepare(None, '/tmp/test.file')
        ok_(rv is True, 'returned %s' % rv)


class TestCommitFalse:
    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.side_effect = Mock(side_effect=OSError)

    def test_fail(self):
        rv = soy.commit('/tmp/', '/tmp/', **{})
        ok_(rv is False, 'returned %s' % rv)


class TestCommitTrue:
    def setUp(self):
        jinja = patch('jinja2.Template')
        jinja.return_value = True

    def test_pass(self):
        rv = soy.commit('/tmp/test', '/tmp/test', **{})
        ok_(rv == True, 'returned %s' % rv)
