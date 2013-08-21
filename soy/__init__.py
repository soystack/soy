#!/usr/bin/env python

from soy.pdns import Domain, Record
from soy.nginx import Host
from soy.vsftp import User

class init:
	def __init__(self, __salt__, **kwargs):
		self.kwargs = kwargs
		self.salt = __salt__

	def create(self):
		Host(self.salt, **self.kwargs).create()
		Domain(self.salt, **self.kwargs).create()
		Record(self.salt, **self.kwargs).create()
		User(self.salt, **self.kwargs).create()

	def report(self):
		Host(self.salt, **self.kwargs).report()
		Domain(self.salt, **self.kwargs).report()
		Record(self.salt, **self.kwargs).report()
		User(self.salt, **self.kwargs).report()

	def update(self):
		Domain(self.salt, **self.kwargs).update()
		Record(self.salt, **self.kwargs).update()
		User(self.salt, **self.kwargs).update()

	def delete(self):
		Host(self.salt, **self.kwargs).delete()
		Domain(self.salt, **self.kwargs).delete()
		Record(self.salt, **self.kwargs).delete()
		User(self.salt, **self.kwargs).delete()

	def suspend_all(self):
		Host(self.salt, **self.kwargs).suspend()

	def unsuspend_all(self):
		Host(self.salt, **self.kwargs).unsuspend()
