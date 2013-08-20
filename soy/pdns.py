#!/usr/bin/env python

import MySQLdb
import time
import soy.utils as soy

class DNS(object):
	def __init__(self, __salt__, **kwargs):
		self.salt = __salt__
		self.pillar = __salt__['pillar.raw']
		self.mysql = {
			'host': self.pillar('mysql.host'),
			'port': self.pillar('mysql.port'),
			'user': self.pillar('mysql.user'),
			'passwd': self.pillar('mysql.pass'),
			'db': self.pillar('pdns-master')['db']}

		self.domains = {}

		self.last_check = str(time.time()).split('.')[0]
		self.name = kwargs.get('name', None)
		self.d_id = kwargs.get('d_id', None)
		self.e_id = kwargs.get('e_id', None)
		self.ttl  = kwargs.get('ttl', 300)
		self.master = kwargs.get('master', '127.0.0.1')
		self.serial = kwargs.get('serial', 1)
		self.e_type = kwargs.get('e_type', 'MASTER')
		self.account = kwargs.get('account', 'EXTERN')
		self.prio = kwargs.get('prio', 0)

		self.serial += 1
		self.notified_serial = self.serial

		self.domains['name'] = self.name
		self.domains['master'] = self.master
		self.domains['notified_serial'] = self.serial
		self.domains['type'] = self.e_type
		self.domains['account'] = self.account
		self.domains['last_check'] = self.last_check

		if self.ttl < 300: self.ttl = 300

	def dbconnect(self):
		try:
			self.db = MySQLdb.connect(**self.mysql)
			self.curs = self.db.cursor()
			return {'status': True}
		except:
			return {'status': False}

class Domain(DNS):
	def create(self):
		try:
			connection = self.dbconnect()
			query = """INSERT INTO domains (`id`, `name`, `master`, `last_check`, `type`, `notified_serial`, `account`)
					   VALUES (NULL, %(name)s, %(master)s, %(last_check)s, %(type)s, %(notified_serial)s, %(account)s)"""
			self.curs.execute(query, self.domains)
			self.db.commit()
			return {'status': True}
		except:
			return {'status': False}

	def report(self):
		try:
			connection = self.dbconnect()
			query = """SELECT * FROM domains"""
			self.db.query(query)
			res = self.db.store_result()
			return res.fetch_row(maxrows=0, how=1)
		except:
			return {'status': False}

	def search(self):
		try:
			connection = self.dbconnect()
			query = """SELECT * FROM domains WHERE `name` REGEXP %s ORDER BY `name` DESC"""
			self.curs.execute(query, (self.name,))
			return self.curs.fetchall()
		except:
			return {'status': False}

	def update_diff(self, defaults):
		try:
			changes = {}
			for pos, field in enumerate(
					['id', 'name', 'master', 'last_check',
					 'type','notified_serial','account']):
				if hasattr(self, field):
					if defaults[pos] is not getattr(self, field):
						changes[field] = getattr(self, field)
				else:
					changes[field] = defaults[pos]
			return changes
		except:
			return {'status': False}

	def update(self):
		try:
			connection = self.dbconnect()
			query = """SELECT * FROM domains WHERE `name`=%s AND `id`=%s"""
			self.curs.execute(query, (self.name, self.e_id,))
			row = self.curs.fetchone()
			defaults = self.update_diff(row)
			query = """UPDATE domains
							SET `account`=%(account)s, 
								`id`=%(id)s,
								`last_check`=%(last_check)s,
								`master`=%(master)s,
								`name`=%(name)s,
								`notified_serial`=%(notified_serial)s,
								`type`=%(type)s  WHERE `id`=%(id)s"""
			self.curs.execute(query, defaults)
			self.db.commit()
			return {'status': True}
		except:
			return {'status': False}

	def delete(self):
		try:
			connection = self.dbconnect()
			query = """DELETE FROM domains WHERE `id`=%s"""
			self.curs.execute(query, (self.e_id,))
			self.db.commit()
			return {'status': True}
		except:
			return {'status': False}

class Record(DNS):
	def create(self):
		try:
			connection = self.dbconnect()
			mail = 'mail.%s' % self.name
			dns = 'dns.%s' % self.name
			host = 'hostmaster.%s' % self.name
		
			args = [(self.d_id, self.name, 'MX', mail, self.ttl, self.prio, self.last_check),
					(self.d_id, mail, 'CNAME', self.name, self.ttl, self.prio, self.last_check),
					(self.d_id, self.name, 'SOA', ". ".join([dns, host]), self.ttl, self.prio, self.last_check)]
			query = """INSERT INTO records (`id`, `domain_id`, `name`, `type`, `content`, `ttl`, `prio`, `change_date`, `ordername`, `auth`)
					   VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, NULL, NULL)"""
			self.curs.executemany(query, args)
			self.db.commit()
			return {'status': True}
		except:
			return {'status': False}

	def report(self):
		try:
			connection = self.dbconnect()
			query = """SELECT * FROM records"""
			self.db.query(query)
			res = self.db.store_result()
			return res.fetch_row(maxrows=0, how=1)
		except:
			return {'status': False}

	def search(self):
		try:
			connection = self.dbconnect()
			query = """SELECT * FROM records WHERE `name` REGEXP %s ORDER BY `name` DESC"""
			self.curs.execute(query, (self.name,))
			return self.curs.fetchall()
		except:
			return {'status': False}

	def update_diff(self, defaults):
		try:
			changes = {}
			for pos, field in enumerate(
					['id','domain_id', 'name', 'type',
					 'content', 'ttl', 'prio', 'change_date',
					 'ordername', 'auth']):
				if hasattr(self, field):
					if defaults[pos] is not getattr(self, field):
						changes[field] = getattr(self, field)
				else:
					changes[field] = defaults[pos]

			return changes
		except:
			return {'status': False}

	def update(self):
		try:
			connection = self.dbconnect()
			query = """UPDATE records SET `name`=%s WHERE `id`=%s"""
			self.curs.execute(query, (self.name, self.e_id,))
			self.db.commit()
			return {'status': True}
		except:
			return {'status': False}

	def delete(self):
		try:
			connection = self.dbconnect()
			query = """DELETE FROM records WHERE `id`=%s"""
			self.curs.execute(query, (self.e_id,))
			self.db.commit()
			return {'status': True}
		except:
			return {'status': False}
	
