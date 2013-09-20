#!/usr/bin/env python

class Setup:
	def __init__(self, __salt__, db):
		self.mysql	= {
            'host'   : __salt__['pillar.raw']('mysql.host'),
            'port'   : __salt__['pillar.raw']('mysql.port'),
            'user'   : __salt__['pillar.raw']('mysql.user'),
            'passwd' : __salt__['pillar.raw']('mysql.pass'),
            'db'     : __salt__['pillar.raw'](db)['db']}
