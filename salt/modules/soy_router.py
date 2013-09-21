#!/usr/bin/env python

import ast
from soy import *

def call(p, c, kwargs):
	a = getattr(p, c)
	if kwargs:
		return a(**kwargs)
	else:
		return a()

def route(service, module, method, opts):
	'''
	router function
	
	CLI Example::

		from salt.client import LocalClient

		kwargs = {'user': 'testuser', 'pswd': 'testpswd'}

		LocalClient.cmd( minion, 'soy_router.route', ['service_name', 'class_name', 'method_name', kwargs] )

	'''
	kwargs = ast.literal_eval(opts)
	service = call( globals()[service], module, kwargs)
	return call(service, method)

	'''
	soy.Nginx.Host(**kwargs).create()
	
	
	base = getattr(soy, service)
	mid = getattr(base, module)(__salt__, **kwargs)
	top = getattr(mid, method)()
	'''
	
	#return getattr( getattr( getattr(soy, service), module )(__salt__, **kwargs), method )()
