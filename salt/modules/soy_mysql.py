def setup(user=False, db='mysql.'):
    if user:
        __pillar__ = __pillar__[user]
	mysql = {'host'	 : __pillar__['mysql.host'],
		 'port'	 : __pillar__['mysql.port'],
		 'user'	 : __pillar__['mysql.user'],
		 'passwd': __pillar__['mysql.pass'],
		 'db':     __pillar__['mysql.db']}

	return mysql
