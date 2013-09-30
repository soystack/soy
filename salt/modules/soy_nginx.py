#!/usr/bin/env python

'''
soy nginx package for creating and deleting host configuration files.
'''

from os import listdir

def mkconf(**sls):
	'''
	write and symlink nginx host files from template.
	'''
	try:
		available = '%s%s.conf' % (__pillar__['nginx']['available'], sls['host'])
		enabled = '%s%s.conf' % (__pillar__['nginx']['enabled'], sls['host'])
		__salt__['soy_utils.commit'](__pillar__['nginx']['template'], available, **sls)
		__salt__['file.symlink'](available, enabled)
		return True
	except (OSError, IOError):
		return False

def mksource(htdocs, **sls):
	'''
	write source html template (placeholders)
	'''
	try:
		path = '%s%s' % (htdocs, 'index.html')
		__salt__['soy_utils.commit'](__pillar__['nginx']['index'], path, **sls)
		__salt__['nginx.signal']('reload')
		return True
	except (OSError, IOError):
		raise OSError

def mkdir(htdocs, **sls):
	'''
	create htdocs directory
	'''
	try:
		__salt__['file.mkdir'](htdocs)
		mksource(htdocs, **sls)
		return True
	except (OSError, IOError):
		return False

def mklog(logdir):
	'''
	write log files in specified log directory
	'''
	try:
		__salt__['file.mkdir'](logdir)
		access = '%s%s' % (logdir, 'access.log')
		error = '%s%s' % (logdir, 'error.log')
		__salt__['soy_utils.prepare'](None, access, error)
		return True
	except (OSError, IOError):
		return False

def delete(user, host, user_root=False):
	'''
	remove host tree
	'''
	try:
		enabled = '%s%s.conf' % (__pillar__['nginx']['enabled'], host)
		available = '%s%s.conf' % (__pillar__['nginx']['available'], host)
		base = '%s%s/' % (__pillar__['nginx']['base'], user)
		if user_root is True:
			__salt__['file.remove'](base)
		__salt__['file.remove'](available)
		__salt__['file.remove'](enabled)
		__salt__['file.remove']('%s%s' % (base, host))
		__salt__['nginx.signal']('reload')
		return True
	except (OSError, IOError, KeyError):
		return False

def create(user, host):
	'''
	build host tree
	'''
	root = '%s%s/%s' % (__pillar__['nginx']['base'], user, host)
	htdocs = '%s%s' % (root, __pillar__['nginx']['htdocs'])
	logdir = '%s%s' % (root, __pillar__['nginx']['logs'])
	try:
		sls = {'user': user, 'host': host}
		mkdir(htdocs, **sls)
		mklog(logdir)
		mkconf(**sls)
		__salt__['nginx.signal']('reload')
		return True
	except (OSError, IOError, KeyError, AttributeError):
		return delete(user, host)

def report(user):
	'''
	report domains owned by user
	'''
	try:
		hosts = {}
		user_root = '%s%s' % (__pillar__['nginx']['base'], user)
		for pos, host in enumerate(listdir(user_dir)):
			try:
				hosts[user][pos] = host
			except:
				return False
			return hosts
	except:
		return False

def update(user, host, updated_host):
	'''
	update domains owned by user
	'''
	try:
		user_root = '%s%s' % (__pillar__['nginx']['base'], user)
		old_domain = '%s%s' % (user_root, host)
		new_domain = '%s%s' % (user_root, updated_host)
		__salt__['file.rename'](old_domain, new_domain)
		return {'status': True}
	except:
		return {'status': False}

def suspend(**sls):
	'''
	suspend users and their hosts
	'''
	try:
		path = '%s%s.conf' % (__pillar__['nginx']['available'], sls['host'])
		link = '%s%s.conf' % (__pillar__['nginx']['enabled'], sls['host'])
		__salt__['file.remove'](link)
		__salt__['file.remove'](path)
		__salt__['soy_utils.commit'](__pillar__['nginx']['susconf'], path, **sls)
		__salt__['file.symlink'](path, link)
		__salt__['nginx.signal']('reload')
		return True
	except (OSError, IOError):
		return False

def unsuspend(**sls):
	'''
	lift suspension
	'''
	try:
		path = '%s%s.conf' % (__pillar__['nginx']['available'], sls['host'])
		link = '%s%s.conf' % (__pillar__['nginx']['enabled'], sls['host'])
		__salt__['file.remove'](link)
		__salt__['file.remove'](path)
		mkconf(**sls)
		__salt__['nginx.signal']('reload')
		return True
	except (OSError, IOError):
		return False
