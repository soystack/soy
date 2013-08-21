#!/usr/bin/env python

from soy.pdns import Domain, Record

def create_domain(self):
	return Domain(__salt__, **kwargs).create()

def report_domain(self):
	return Domain(__salt__, **kwargs).report()

def update_domain(self):
	return Domain(__salt__, **kwargs).update()

def delete_domain(self):
	return Domain(__salt__, **kwargs).delete()

def create_record(self):
	return Record(__salt__, **kwargs).create()

def report_record(self):
	return Record(__salt__, **kwargs).report()

def update_record(self):
	return Record(__salt__, **kwargs).update()

def delete_record(self):
	return Record(__salt__, **kwargs).delete()
