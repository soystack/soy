#!/usr/bin/env python

'''
soy ftp package for file and user editing
'''

from ftplib import FTP
from bsddb import db

class User(object):
	'''
	init
	'''
	def __init__(self, __salt__, **kwargs):
		self.salt = __salt__
		self.user = kwargs.get('user', 'undefined')
		self.pswd = kwargs.get('pswd', 'undefined')
		self.newuser = kwargs.get('newuser', 'undefined')
		self.newpswd = kwargs.get('newpswd', 'undefined')

		def _connect():
			'''
			connect to vsftp user db
			'''
			self.userdb = db.DB()
			self.userdb.open('/etc/vsftpd/vsftpd-virtual-user.db',
							  db.DB_HASH,
							  db.DB_DIRTY_READ)

		def _transfer_content(user, newuser):
			self.salt['cmd.run']('cp -rf /home/vftp/%s/* /home/vftp/%s/' % (user, newuser))

		self.connect = _connect
		self.transfer_content = _transfer_content

	def create(self):
		'''
		create new user
		'''
		try:
			if self.newuser is 'undefined':
				user = self.user
				pswd = self.pswd
			else:
				user = self.newuser
				pswd = self.newpswd

			self.connect()
			self.userdb.put(user, pswd)
			self.userdb.close()
			self.salt['cmd.run']('mkdir -p /home/vftp/%s' % user)
			return {'status': True}
		except:
			return {'status': False}

	def report(self):
		'''
		return a list of users
		'''
		try:
			users = {}
			self.connect()
			cursor = self.userdb.cursor()
			rec = cursor.first()
			if isinstance(rec, tuple):
				while rec:
					users[rec[0]] = rec[1]
					rec = cursor.next()
			self.userdb.close()
			return users
		except:
			return {'status': False}

	def update(self):
		'''
		update user data
		'''
		try:
			self.create()
			self.transfer_content(self.user, self.newuser)
			self.delete()
			return {'status': True}
		except:
			return {'status': False}

	def delete(self):
		'''
		delete user
		'''
		try:
			self.connect()
			self.userdb.delete(self.user)
			self.userdb.close()
			self.salt['file.remove']('/home/vftp/%s' % self.user)
			return {'status': True}
		except:
			return {'status': False}

