#!/usr/bin/env python

'''
soy ftp package for file and user editing
'''

from ftplib import FTP
from bsddb import db

def connect():
	'''
	connect to vsftp user db
	'''
	userdb = db.DB()
	userdb.open('/etc/vsftpd/vsftpd-virtual-user.db', db.DB_HASH, db.DB_DIRTY_READ)
	return userdb

def transfer_content(user, newuser):
	__salt__['cmd.run']('cp -rf /home/vftp/%s/* /home/vftp/%s/' % (user, newuser))

def create(user, pswd):
	'''
	create new user
	'''
	try:
		userdb = connect()
		userdb.put(user, pswd)
		userdb.close()
		__salt__['cmd.run']('mkdir -p /home/vftp/%s' % user)
		return {'status': True}
	except:
		return {'status': False}

def report():
	'''
	return a list of users
	'''
	try:
		users = {}
		userdb = connect()
		cursor = userdb.cursor()
		rec = cursor.first()
		if isinstance(rec, tuple):
			while rec:
				users[rec[0]] = rec[1]
				rec = cursor.next()
		userdb.close()
		return users
	except:
		return {'status': False}

def update(user, newuser, newpswd):
	'''
	update user data
	'''
	try:
		connect()
		create(newuser, newpswd)
		transfer_content(user, newuser)
		delete(user)
		return {'status': True}
	except:
		return {'status': False}

def delete(user):
	'''
	delete user
	'''
	try:
		userdb = connect()
		userdb.delete(user)
		userdb.close()
		__salt__['file.remove']('/home/vftp/%s' % user)
		return {'status': True}
	except:
		return {'status': False}

