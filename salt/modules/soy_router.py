#!/usr/bin/env python

from soy import *

def call(p, c, **kwargs):
	c = getattr(p, c)
	if kwargs:
		return c(**kwargs)
	else:
		return c()

def route(service, module, method, kwargs):
	'''
	router function
	
	CLI Example::

		from salt.client import LocalClient

		kwargs = {'user': 'testuser', 'pswd': 'testpswd'}

		LocalClient.cmd( minion, 'soy_router.route', ['service_name', 'class_name', 'method_name', kwargs] )

	'''
	
	service = call( globals()[service], module, **kwargs)
	return call(service, method)

	'''
	soy.Nginx.Host(**kwargs).create()
	
	
	base = getattr(soy, service)
	mid = getattr(base, module)(__salt__, **kwargs)
	top = getattr(mid, method)()
	'''
	
	#return getattr( getattr( getattr(soy, service), module )(__salt__, **kwargs), method )()
