#!/usr/bin/env python

from soy.vsftp import User

def create(kwargs):
	return User(__salt__, **kwargs).create()

def report(kwargs):
	return User(__salt__, **kwargs).report()

def update(kwargs):
	return User(__salt__, **kwargs).update()

def delete(kwargs):
	return User(__salt__, **kwargs).delete()
