#!/usr/bin/env python

from soy.pdns import dns

class domain(object):
	def __init__(self, **kwargs):
		self.dns = Domain(__salt__, **kwargs)

	def create(self):
		return self.dns.create_domain()

	def report(self):
		return self.dns.report_domain()

	def update(self):
		return self.dns.update_domain()

	def delete(self):
		return self.dns.delete_domain()

class record(object):
	def __init__(self, **kwargs):
		self.dns = Record(__salt__, **kwargs)

	def createRecord(self):
		return self.dns.createRecord()

	def reportRecord(self):
		return self.dns.reportRecord()

	def updateRecord(self):
		return self.dns.updateRecord()

	def deleteRecord(self):
		return self.dns.deleteRecord()

