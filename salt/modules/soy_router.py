#!/usr/bin/env python

from soy import *

def route(service, module, method, opts):
	'''
	router function
	
	CLI Example::

		from salt.client import LocalClient

		kwargs = {'user': 'testuser', 'pswd': 'testpswd'}

		LocalClient.cmd( minion, 'soy_router.route', ['service_name', 'class_name', 'method_name', kwargs] )

	'''
	lib = 'soy.%s' % service
	eval 'from %s import %s' % module
	getattr(globals()[module](**kwargs), method)()

	'''
	soy.Nginx.Host(**kwargs).create()
	
	
	base = getattr(soy, service)
	mid = getattr(base, module)(__salt__, **kwargs)
	top = getattr(mid, method)()
	'''
	
	#return getattr( getattr( getattr(soy, service), module )(__salt__, **kwargs), method )()
