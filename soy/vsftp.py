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
	def __init__(self, **kwargs):
		self.user = kwargs.get('user', 'undefined')
		self.pswd = kwargs.get('pswd', 'undefined')

		def _connect():
			'''
			connect to vsftp user db
			'''
			self.userdb = db.DB()
			self.userdb.open('/etc/vsftpd/vsftpd-virtual-user.db',
							  db.DB_HASH,
							  db.DB_DIRTY_READ)

		self.connect = _connect

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

	def create(self):
		'''
		create new user
		'''
		try:
			self.connect()
			self.userdb.put(self.user, self.pswd)
			self.userdb.close()	
			return {'status': True}
		except:
			return {'status': False}
