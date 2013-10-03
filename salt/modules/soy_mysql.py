def setup(user=False, db='mysql.'):
    if user:
        __pillar__ = __pillar__[user]
	mysql = {
		'host'	 : __pillar__['mysql.host'],
		'port'	 : __pillar__['mysql.port'],
		'user'	 : __pillar__['mysql.user'],
		'passwd' : __pillar__['mysql.pass']
	}
    if db is not 'mysql.':
        db = '%s.' % db
    mysql['db'] = __pillar__[db+'db']
	return mysql
