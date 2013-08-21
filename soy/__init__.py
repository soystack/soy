#!/usr/bin/env python

from soy.pdns import Domain, Record
from soy.nginx import Host
from soy.vsftp import User

class init:
	def __init__(self):

	def create(self):
		Host(__salt__, **kwargs).create()
		Domain(__salt__, **kwargs).create()
		Record(__salt__, **kwargs).create()
		User(__salt__, **kwargs).create()

	def report(self):
		__salt__['pillar.raw']('nginx')
		Domain(__salt__, **kwargs).report()
		Record(__salt__, **kwargs).report()
		User(__salt__, **kwargs).report()

	def update(self):
		Domain(__salt__, **kwargs).update()
		Record(__salt__, **kwargs).update()
		User(__salt__, **kwargs).update()

	def delete(self):
		Host(__salt__, **kwargs).delete()
		Domain(__salt__, **kwargs).delete()
		Record(__salt__, **kwargs).delete()
		User(__salt__, **kwargs).delete()

	def suspend_all(self):
		Host(__salt__, **kwargs).suspend()

	def unsuspend_all(self):
		Host(__salt__, **kwargs).unsuspend()
