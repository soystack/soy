#!/usr/bin/env python

from soy.vsftp import User

class user(object):
	def __init__(self, **kwargs):
		self.ftp = User(__salt__, **kwargs)

	def create(self):
		return self.ftp.create()

	def report(self):
		return self.ftp.report()

	def update(self):
		return self.ftp.update()

	def delete(self):
		return self.ftp.delete()

def start_ftp(kwargs):
	return getattr(user(**kwargs), kwargs['func'])()
