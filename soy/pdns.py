import MySQLdb
import soy.utils as soy
import time

class DNS(object):
    def __init__(self, __salt__, **kwargs):
        self.mysql  = {
            'host'   : __salt__['pillar.raw']('mysql.host'),
            'port'   : __salt__['pillar.raw']('mysql.port'),
            'user'   : __salt__['pillar.raw']('mysql.user'),
            'passwd' : __salt__['pillar.raw']('mysql.pass'),
            'db'     : __salt__['pillar.raw']('pdns-master')['db']}

	for k, v in kwargs.iteritems():
		setattr(self, k, kwargs.get(v, 'undefined'))
		
	"""
	for k, v in kwargs.iteritems():
		self.pillar[k] = v
	"""

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

    def update(self):
        try:
            connection = self.dbconnect()
            query = """UPDATE domains
                       SET `account`=%(account)s,
                           `id`=%(id)s,
                           `last_check`=%(last_check)s,
                           `master`=%(master)s,
                           `name`=%(name)s,
                           `notified_serial`=%(notified_serial)s,
                           `type`=%(type)s  WHERE `id`=%(id)s"""
            self.curs.execute(query, self)
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

	def update(self):
		try:
			connection = self.dbconnect()
			query = """SELECT * FROM domains WHERE `name`=%s AND `id`=%s"""
			self.curs.execute(query, (self.name, self.e_id,))
			row = self.curs.fetchone()
			defaults = self.update_diff(row)
			"""
			# A Proposal
			for k, v in self.pillar.iteritems():
				query = """UPDATE domains SET `%s`=%(%s)s WHERE `id`=%(id)s""" % (k,v)
				self.curs.execute(query, self.pillar)
				self.db.commit()
			return {'status': True}
			"""
			query = """UPDATE domains
					   SET `id`=%(account)s,
					   `domain_id`=%(id)s,
					   `name`=%(last_check)s,
					   `type`=%(master)s,
					   `content`=%(name)s,
					   `ttl`=%(notified_serial)s,
					   `prio`=%(type)s,
					   `change_date`=(change_date)s,
					   `ordername`=%(ordername)s,
					   `auth`=%(auth)s WHERE `id`=%(id)s"""
			self.curs.execute(query, self)
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

