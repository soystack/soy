try:
    from warnings import warn
except:
    warn = print
try:
    import MySQLdb as sql
except ImportError:
    warn('MySQL-python must be installed', ImportWarning)
    exit()

def connect(db=None):
    try:
        sqlconf = __salt__['soy_mysql.setup'](db)
        conn = sql.connect(**sqlconf)
        curs = sql.cursor()
        return conn, curs
    except sql.Error as e:
        return False, 'mysql connection error: %s' % e.message
    except:
        warn('error while establishing connection', RuntimeWarning)
        return False
    finally:
        if conn:
            conn.close()

def grant(**opts):
    try:
        conn, curs = connect(opts['db'])
        permset = str()
        for eachtype in opts['perms']:
            permset += '%s,' % eachtype
        opts['perms'] = permset[:-1]
        curs.execute('''GRANT %(perms)s ON %(db)s.%(table)s TO "%(user)s"@"%(ip)s"''', **opts)
        return True
    except sql.Error as e:
        return False, 'mysql error: %s' % e.message
    except:
        warn('error while granting permissions', RuntimeWarning)
        return False
    finally:
        conn.close()

def adduser(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''CREATE USER "%(user)s"@"%(ip)s" IDENTIFIED BY "%(passwd)s";
                        GRANT SELECT, INSERT ON %(db)s.%(table)s TO "%(user)s"@"%(ip)s";
                        GRANT USAGE ON %(db)s.%(table)s
                        TO "%(user)s"@"%(ip)s" WITH MAX_QUERIES_PER_HOUR 100''', **opts)
    except sql.Error as e:
        return False, 'mysql error: %s' % e.message
    except:
        warn('error while creating user', RuntimeWarning)
        return False
    finally:
        conn.close()

def deleteuser(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''DROP USER %(user)s@%(ip)s''', **opts)
    except sql.Error as e:
        return False, 'mysql error: %s' % e.message
    except:
        warn('error while deleting user', RuntimeWarning)
        return False
    finally:
        conn.close()

def update(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''UPDATE %(db)s.%(table) SET %(key)s = %(value)s WHERE %(cond)s = %(exp)s''', **opts)
    except sql.Error as e:
        return False, 'mysql error: %s' % e.message
    except:
        warn('error while updating field', RuntimeWarning)
        return False
    finally:
        conn.close()

def report(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''SELECT %(column)s FROM %(db)s.%(table)s WHERE $(cond)s = %(exp)s''', **opts)
    except sql.Error as e:
        return False, 'mysql error: %s' % e.message 
    except:
        warn('error while reporting rows', RuntimeWarning)
        return False
    finally:
        conn.close()

def deleterow(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''DROP FROM %(db)s.%(table)s WHERE %(cond)s = %(exp)s''', **opts)
    except sql.Error as e:
        return False, 'mysql error: %s' % e.message
    except:
        warn('error while deleting row', RuntimeWarning)
        return False
    finally:
        conn.close()

def dropdb(**opts):
    try:
        conn, curs = connect()
        curs.execute('''DROP DATABASE %(db)s''', **opts)
    except sql.Error as e:
        return False, 'mysql error: %s' % e.message
    except:
        warn('error while dropping db. most likely syntax related', UserWarning)
        return False
    finally:
        conn.close()

def createdb(**opts):
    try:
        conn, curs = connect()
        curs.execute('''CREATE DATABASE IF NOT EXISTS %(db)s;
                        GRANT ALL ON %(db)s.* TO "%(user)s"@"%(ip)s";''', **opts)
        return True
    except sql.Error as e:
        return False, 'mysql error: %s' % e.message
    except:
        warn('error while creating db', RuntimeWarning)
        return False
    finally:
        conn.close()

def createtable(**opts):
    try:
        conn, curs = connect(opts['db'])
        query = ''
        for k, v in opts['fields'].iteritems():
            '''
            example k, v:
                k => 'id'
                v => 'INT AUTO_INCREMENT'
            '''
            query += '%s %s,' % (k, v)
        opts['fields'] = query[:-1]
        curs.execute('''CREATE TABLE %(db)s.%(table)s (%(fields)s)''', **opts)
        return True
    except sql.Error as e:
        return False, 'mysql error: %s' % e.message
    except:
        warn('error whilst creating table', RuntimeWarning)
        return False
    finally:
        conn.close()
