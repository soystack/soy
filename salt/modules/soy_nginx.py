#!/usr/bin/env python

'''
soy nginx package for creating and deleting host configuration files.
'''

import soy.utils as soy
from os import listdir

salt, pillar = {}, {}


def loadsalt():
	global salt, pillar
	salt = __salt__
	pillar = salt['pillar.raw']('nginx')

def mkconf(**sls):
	'''
	write and symlink nginx host files from template.
	'''
	try:
		available = '%s%s.conf' % (pillar['available'], sls['host'])
		enabled = '%s%s.conf' % (pillar['enabled'], sls['host'])
		soy.commit(pillar['template'], available, **sls)
		salt['file.symlink'](available, enabled)
		return True
	except (OSError, IOError):
		return False

def mksource(htdocs, **sls):
	'''
	write source html template (placeholders)
	'''
	try:
		path = '%s%s' % (htdocs, 'index.html')
		soy.commit(pillar['index'], path, **sls)
		salt['nginx.signal']('reload')
		return True
	except (OSError, IOError):
		raise OSError

def mkdir(htdocs, **sls):
	'''
	create htdocs directory
	'''
	try:
		salt['file.mkdir'](htdocs)
		if pillar['index']:
			mksource(htdocs, **sls)
		return True
	except (OSError, IOError):
		return False

def mklog(logdir):
	'''
	write log files in specified log directory
	'''
	try:
		salt['file.mkdir'](logdir)
		access = '%s%s' % (logdir, 'access.log')
		error = '%s%s' % (logdir, 'error.log')
		soy.prepare(None, access, error)
		return True
	except (OSError, IOError):
		return False

def delete(user, host, user_root=False):
	'''
	remove host tree
	'''
	if not globals()['salt']:
		loadsalt()
	try:
		enabled = '%s%s.conf' % (pillar['enabled'], host)
		available = '%s%s.conf' % (pillar['available'], host)
		base = '%s%s/' % (pillar['base'], user)
		if user_root is True:
			salt['file.remove'](base)
		salt['file.remove'](available)
		salt['file.remove'](enabled)
		salt['file.remove']('%s%s' % (base, host))
		salt['nginx.signal']('reload')
		return True
	except (OSError, IOError, KeyError):
		return False

def create(user, host):
	'''
	build host tree
	'''
	loadsalt()
	root = '%s%s/%s' % (pillar['base'], user, host)
	htdocs = '%s%s' % (root, pillar['htdocs'])
	logdir = '%s%s' % (root, pillar['logs'])
	try:
		sls = {'user': user, 'host': host}
		mkdir(htdocs, **sls)
		mklog(logdir)
		mkconf(**sls)
		salt['nginx.signal']('reload')
		return True
	except (OSError, IOError, KeyError, AttributeError):
		return delete(user, host)

def report(user):
	'''
	report domains owned by user
	'''
	loadsalt()
	try:
		hosts = {}
		user_root = '%s%s' % (pillar['base'], user)
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
	loadsalt()
	try:
		user_root = '%s%s' % (pillar['base'], user)
		old_domain = '%s%s' % (user_root, host)
		new_domain = '%s%s' % (user_root, updated_host)
		salt['file.rename'](old_domain, new_domain)
		return {'status': True}
	except:
		return {'status': False}

def suspend(**sls):
	'''
	suspend users and their hosts
	'''
	loadsalt()
	try:
		path = '%s%s.conf' % (pillar['available'], sls['host'])
		link = '%s%s.conf' % (pillar['enabled'], sls['host'])
		salt['file.remove'](link)
		salt['file.remove'](path)
		soy.commit(pillar['susconf'], path, **sls)
		salt['file.symlink'](path, link)
		salt['nginx.signal']('reload')
		return True
	except (OSError, IOError):
		return False

def unsuspend(**sls):
	'''
	lift suspension
	'''
	loadsalt()
	try:
		path = '%s%s.conf' % (pillar['available'], sls['host'])
		link = '%s%s.conf' % (pillar['enabled'], sls['host'])
		salt['file.remove'](link)
		salt['file.remove'](path)
		mkconf(**sls)
		salt['nginx.signal']('reload')
		return True
	except (OSError, IOError):
		return False
