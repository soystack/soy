#!/usr/bin/env python

def route(service, module, method, opts):
	'''
	router function
	
	CLI Example::

		from salt.client import LocalClient

		kwargs = {'user': 'testuser', 'pswd': 'testpswd'}

		LocalClient.cmd( minion, 'soy_router.route', ['service_name', 'class_name', 'method_name', kwargs] )

	'''
	eval 'from soy.%s import %s' % (service, module)
	getattr(globals()[module](**kwargs), method)()
