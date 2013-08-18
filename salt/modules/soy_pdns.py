#!/usr/bin/env python

from soy.pdns import dns

class domain(object):
	def __init__(self, **kwargs):
		self.dns = Domain(__salt__, **kwargs)

	def create(self):
		return self.dns.create()

	def report(self):
		return self.dns.report()

	def update(self):
		return self.dns.update()

	def delete(self):
		return self.dns.delete()

class record(object):
	def __init__(self, **kwargs):
		self.dns = Record(__salt__, **kwargs)

	def create(self):
		return self.dns.create()

	def report(self):
		return self.dns.report()

	def update(self):
		return self.dns.update()

	def delete(self):
		return self.dns.delete()

