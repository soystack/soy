#!/usr/bin/env python

def setup(db):
	mysql = {
		'host'	 : __pillar__('mysql.host'),
		'port'	 : __pillar__('mysql.port'),
		'user'	 : __pillar__('mysql.user'),
		'passwd' : __pillar__('mysql.pass'),
		'db'	 : __pillar__[db]['db']
	}
	return mysql
