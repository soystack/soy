#!/usr/bin/env python

from soy.vsftp import User

def create(self):
	return User(__salt__, **kwargs).create()

def report(self):
	return User(__salt__, **kwargs).report()

def update(self):
	return User(__salt__, **kwargs).update()

def delete(self):
	return User(__salt__, **kwargs).delete()
