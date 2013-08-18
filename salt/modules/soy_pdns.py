#!/usr/bin/env python

from soy.pdns import Domain, Record

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

def start_domain(kwargs):
	func = kwargs.get('func', None)
	for attr in dir(domain):
		if func is attr:
			return getattr(domain(**kwargs), func)()

	return {'status': 'function %s failed' % func}
		

def start_record(func, **kwargs):
	func = kwargs.get('func', None)
	for attr in dir(record):
		if func is attr:
			return getattr(record(**kwargs), func)()

	return {'status': 'function %s failed' % func}
