#!/usr/bin/env python

from soy.pdns import dns

def createDomain(name):
	kwargs = {'name': name}
	cli = dns(__salt__, **kwargs)
	return cli.createDomain()

def reportDomain():
	kwargs = {}
	cli = dns(__salt__, **kwargs)
	return cli.reportDomain()

def updateDomain(**kwargs):
	cli = dns(__salt__, **kwargs)
	return cli.updateDomain()

def deleteDomain(id):
	kwargs = {'id': id}
	cli = dns(__salt__, **kwargs)
	return cli.deleteDomain()

def createRecord(**kwargs):
	cli = dns(__salt__, **kwargs)
	return cli.createRecord()

def reportRecord():
	kwargs = {}
	cli = dns(__salt__, **kwargs)
	return cli.reportRecord()


def updateRecord(name, id):
	kwargs = {'name': name,
			  'id': id}
	cli = dns(__salt__, **kwargs)
	return cli.updateRecord()


def deleteRecord(id):
	kwargs = {'id': id}
	cli = dns(__salt__, **kwargs)
	return cli.deleteRecord()

