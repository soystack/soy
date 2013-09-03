#!/usr/bin/env python

'''
soy nginx package for creating and deleting host configuration files.
'''

import soy.utils as soy
from os import listdir


class Host(object):
	'''
	init
	'''
	def __init__(self, __salt__, **kwargs):
		self.salt = __salt__
		self.pillar = self.salt['pillar.raw']('nginx')
		'''
		self.host = kwargs['host']
		self.user = kwargs['user']
		self.updated_host = kwargs['updated_host']
		'''
		for k, v in kwargs.iteritems():
			setattr(self, k, kwargs.get(v, 'undefined'))

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

	def delete(self, user=False):
		'''
		remove host tree
		'''
		try:
			enabled = '%s%s.conf' % (self.pillar['enabled'], self.host)
			available = '%s%s.conf' % (self.pillar['available'], self.host)
			base = '%s%s/' % (self.pillar['base'], self.user)
			if user is True:
				self.salt['file.remove'](base)
			self.salt['file.remove'](available)
			self.salt['file.remove'](enabled)
			self.salt['file.remove']('%s%s' % (base, self.host))
			self.salt['nginx.signal']('reload')
			return True
		except (OSError, IOError, KeyError):
			return False

	def create(self):
		'''
		build host tree
		'''
		root = '%s%s/%s' % (self.pillar['base'],
							self.user,
							self.host)
		htdocs = '%s%s' % (root, self.pillar['htdocs'])
		logdir = '%s%s' % (root, self.pillar['logs'])

		try:
			self.mkdir(htdocs)
			self.mklog(logdir)
			self.mkconf()
			self.salt['nginx.signal']('reload')
			return True
		except (OSError, IOError, KeyError, AttributeError):
			return self.delete()

	def report(self):
		'''
		report domains owned by user
		'''
		try:
			host = {}
			user_root = '%s%s' % (self.pillar['base'], self.user)
			for pos, host in enumerate(listdir(user_dir)):
				hosts[self.user][pos] = host

			return hosts
		except:
			return False

	def update(self):
		'''
		update domains owned by user
		'''
		try:
			user_root = '%s%s' % (self.pillar['base'], self.user)
			old_domain = '%s%s' % (user_root, self.host)
			new_domain = '%s%s' % (user_root, self.updated_host)
			self.salt['file.rename'](old_domain, new_domain)
			return {'status': True}
		except:
			return {'status': False}
	def suspend(self):
		'''
		suspend users and their hosts
		'''
		try:
			path = '%s%s.conf' % (self.pillar['available'], self.host)
			link = '%s%s.conf' % (self.pillar['enabled'], self.host)
			self.salt['file.remove'](link)
			self.salt['file.remove'](path)
			soy.commit(self.pillar['susconf'], path, **self.__dict__)
			self.salt['file.symlink'](path, link)
			self.salt['nginx.signal']('reload')
			return True
		except (OSError, IOError):
			return False

	def unsuspend(self):
		'''
		lift suspension
		'''
		try:
			path = '%s%s.conf' % (self.pillar['available'], self.host)
			link = '%s%s.conf' % (self.pillar['enabled'], self.host)
			self.salt['file.remove'](link)
			self.salt['file.remove'](path)
			self.mkconf()
			self.salt['nginx.signal']('reload')
			return True
		except (OSError, IOError):
			return False
