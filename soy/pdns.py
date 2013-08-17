#!/usr/bin/env python

'''
soy powerdns package for creating and maintaining dns tables.
'''

import MySQLdb

class DNS(object):
	'''
	init
	'''
	def __init__(self, __salt__, **kwargs):
		self.salt = __salt__
		self.pillar = __salt__['pillar.raw']
		self.mysql = {
			'host': self.pillar('mysql.host'),
			'port': self.pillar('mysql.port'),
			'user': self.pillar('mysql.user'),
			'pass': self.pillar('mysql.pass'),
			'db': self.pillar('mysql.db'),
			'unix_socket': self.pillar('mysql.unix_socket')
		}
		self.database = self.curs = None
		self.name = kwargs['name']

	def _connect(self, **kwargs):
		'''
		connect to specified database
		'''
		self.datebase = MySQLdb.connect(**kwargs)
		self.curs = self.database.cursor()

	def insert_domain(self):
		'''
		insert domain into table domains
		'''
		query = '''INSERT INTO domains
				   SET `name`=%s, `type`="MASTER", `account`="EXTER"'''
		self.curs.execute(query, (self.name))

	def insert_record(self):
		'''
		insert record into table records
		'''
		mail = 'mail.%s' % self.name
		dns = 'dns.%s' % self.name
		host = 'hostmaster.%s' % self.name

		args = [(self.name, 'MX', mail),
				(mail, 'CNAME', self.name),
				(self.name, 'SOA', ". ".join([dns, host]))]
		query = """INSERT INTO records (`name`, `type`, `content`)
						VALUES (%s, %s, %s)"""
		self.curs.executemany(query, args)

	def create_domain(self):
		'''
		build insert tree
		'''
		self._connect(**self.mysql)
		self.insert_domain()
		self.insert_record()
