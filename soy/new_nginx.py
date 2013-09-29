#!/usr/bin/env python

'''
soy nginx package for creating and deleting host configuration files.
'''

import soy.utils as soy
from os import listdir

class setup:
	def __init__(self, salt):
		self.salt = salt
		self.pillar = self.salt['pillar.raw']('nginx')
	def __call__(self, fn):
		fn.salt = self.salt
		fn.pillar = self.pillar
		return fn

def mkconf(self):
	'''
	write and symlink nginx host files from template.
	'''
	try:
		available = '%s%s.conf' % (self.pillar['available'], self.host)
		enabled = '%s%s.conf' % (self.pillar['enabled'], self.host)
		soy.commit(self.pillar['template'], available, **self.__dict__)
		self.salt['file.symlink'](available, enabled)
		return True
	except (OSError, IOError):
		return False

def mksource(self, htdocs):
	'''
	write source html template (placeholders)
	'''
	try:
		path = '%s%s' % (htdocs, 'index.html')
		soy.commit(self.pillar['index'], path, **self.__dict__)
		self.salt['nginx.signal']('reload')
		return True
	except (OSError, IOError):
		raise OSError

def mkdir(self, htdocs):
	'''
	create htdocs directory
	'''
	try:
		self.salt['file.mkdir'](htdocs)
		if self.pillar['index']:
			self.mksource(htdocs)
		return True
	except (OSError, IOError):
		return False

def mklog(self, logdir):
	'''
	write log files in specified log directory
	'''
	try:
		self.salt['file.mkdir'](logdir)
		access = '%s%s' % (logdir, 'access.log')
		error = '%s%s' % (logdir, 'error.log')
		soy.prepare(None, access, error)
		return True
	except (OSError, IOError):
		return False

@setup(__salt__)
def delete(user, host, user_root=False):
	'''
	remove host tree
	'''
	try:
		enabled = '%s%s.conf' % (delete.pillar['enabled'], host)
		available = '%s%s.conf' % (delete.pillar['available'], host)
		base = '%s%s/' % (self.pillar['base'], user)
		if user_root is True:
			delete.salt['file.remove'](base)
		delete.salt['file.remove'](available)
		delete.salt['file.remove'](enabled)
		delete.salt['file.remove']('%s%s' % (base, host))
		delete.salt['nginx.signal']('reload')
		return True
	except (OSError, IOError, KeyError):
		return False

@setup(__salt__)
def create(user, host):
	'''
	build host tree
	'''
	root = '%s%s/%s' % (create.pillar['base'], user, host)
	htdocs = '%s%s' % (root, create.pillar['htdocs'])
	logdir = '%s%s' % (root, create.pillar['logs'])
	try:
		create.user = user
		create.host = host
		mkdir(create, htdocs)
		mklog(create, logdir)
		mkconf(create)
		create.salt['nginx.signal']('reload')
		return True
	except (OSError, IOError, KeyError, AttributeError):
		return delete(create.user, create.host)

@setup(__salt__)
def report(user):
	'''
	report domains owned by user
	'''
	try:
		hosts = {}
		user_root = '%s%s' % (report.pillar['base'], user)
		for pos, host in enumerate(listdir(user_dir)):
			try:
				hosts[user][pos] = host
			except:
				return False
			return hosts
	except:
		return False

@setup(__salt__)
def update(user, host, updated_host):
	'''
	update domains owned by user
	'''
	try:
		user_root = '%s%s' % (update.pillar['base'], user)
		old_domain = '%s%s' % (user_root, host)
		new_domain = '%s%s' % (user_root, updated_host)
		update.salt['file.rename'](old_domain, new_domain)
		return {'status': True}
	except:
		return {'status': False}

@setup(__salt__)
def suspend(host):
	'''
	suspend users and their hosts
	'''
	try:
		path = '%s%s.conf' % (suspend.pillar['available'], host)
		link = '%s%s.conf' % (suspend.pillar['enabled'], host)
		suspend.salt['file.remove'](link)
		suspend.salt['file.remove'](path)
		soy.commit(self.pillar['susconf'], path, **suspend.__dict__)
		suspend.salt['file.symlink'](path, link)
		suspend.salt['nginx.signal']('reload')
		return True
	except (OSError, IOError):
		return False

@setup(__salt__)
def unsuspend(host):
	'''
	lift suspension
	'''
	try:
		unsuspend.host = host
		path = '%s%s.conf' % (unsuspend.pillar['available'], host)
		link = '%s%s.conf' % (unsuspend.pillar['enabled'], host)
		unsuspend.salt['file.remove'](link)
		unsuspend.salt['file.remove'](path)
		mkconf(unsuspend)
		unsuspend.salt['nginx.signal']('reload')
		return True
	except (OSError, IOError):
		return False
