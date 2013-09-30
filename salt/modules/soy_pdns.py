try:
	import MySQLdb
	import time
except:
	print 'Must install MySQL-python'

def dns():
	mysql = __salt__['soy_mysql.setup']('pdns')
	try:
		db = MySQLdb.connect(**mysql)
		curs = db.cursor()
		return db, curs
	except:
		return False

def createdomain(**opts):
	try:
		db, curs = dns()
		curs.execute("""INSERT INTO domains
									(`id`,
									 `name`,
									 `master`,
									 `last_check`,
									 `type`,
									 `notified_serial`,
									 `account`)
						 VALUES		 (NULL,
									 %(name)s,
									 %(master)s,
									 %(last_check)s,
									 %(type)s,
									 %(notified_serial)s,
									 %(account)s)""", **opts)
		db.commit()
		return {'status': True}
	except:
		return {'status': False}

def reportdomain():
	try:
		db, curs = dns()
		db.query("""SELECT * FROM domains""")
		res = db.store_result()
		return res.fetch_row(maxrows=0, how=1)
	except:
		return {'status': False}

def searchdomain(name):
	try:
		db, curs = dns()
		curs.execute("""SELECT *
						FROM domains
						WHERE `name` REGEXP %s
		   			    ORDER BY `name` DESC""", (name,))
		return curs.fetchall()
	except:
		return {'status': False}

def updatedomain(**opts):
	try:
		db, curs = dns()
		curs.execute("""UPDATE domains
						SET `account`=%(account)s,
							`id`=%(id)s,
							`last_check`=%(last_check)s,
							`master`=%(master)s,
							`name`=%(name)s,
							`notified_serial`=%(notified_serial)s,
							`type`=%(type)s
						WHERE `id`=%(id)s""", **opts)
		db.commit()
		return {'status': True}
	except:
		return {'status': False}

def deletedomain(e_id):
	try:
		db, curs = dns()
		curs.execute("""DELETE FROM domains WHERE `id`=%s""", (e_id,))
		db.commit()
		return {'status': True}
	except:
		return {'status': False}

def createrecord(name, ttl, prio, last_check, d_id):
	mail = 'mail.%s' % name
	dns  = 'dns.%s' % name
	host = 'hostmaster.%s' % name
	try:
		db, curs = dns()
		args = [(d_id, name, 'MX', mail, ttl, prio, last_check),
				(d_id, mail, 'CNAME', name, ttl, prio, last_check),
				(d_id, name, 'SOA', ". ".join([dns, host]), ttl, prio, last_check)]
		curs.executemany("""INSERT INTO records
										 (`id`,
										  `domain_id`,
										  `name`,
										  `type`,
										  `content`,
										  `ttl`,
										  `prio`,
										  `change_date`,
										  `ordername`,
										  `auth`)"
							 VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, NULL, NULL)""", args)
		db.commit()
		return {'status': True}
	except:
		return {'status': False}

def reportrecord():
	try:
		db, curs = dns()
		db.query("""SELECT * FROM records""")
		res = db.store_result()
		return res.fetch_row(maxrows=0, how=1)
	except:
		return {'status': False}

def searchrecord(name):
	try:
		db, curs = dns()
		curs.execute("""SELECT *
						FROM records
						WHERE `name` REGEXP %s
						ORDER BY `name` DESC""", (self.name,))
		return curs.fetchall()
	except:
		return {'status': False}

def updaterecord(**opts):
	try:
		db, curs = dns()
		curs.execute("""UPDATE domains
						SET `id`=%(account)s,
							`domain_id`=%(id)s,
							`name`=%(last_check)s,
							`type`=%(master)s,
							`content`=%(name)s,
							`ttl`=%(notified_serial)s,
							`prio`=%(type)s,
							`change_date`=%(change_date)s,
							`ordername`=%(ordername)s,
							`auth`=%(auth)s
						WHERE `id`=%(id)s""", **opts)
		db.commit()
		return {'status': True}
	except:
		return {'status': False}

def deleterecord(e_id):
	try:
		db, curs = dns()
		curs.execute("""DELETE FROM records WHERE `id`=%s""", (e_id,))
		db.commit()
		return {'status': True}
	except:
		return {'status': False}
