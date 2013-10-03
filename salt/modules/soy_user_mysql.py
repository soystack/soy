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
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
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
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
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
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while creating user', RuntimeWarning)
        return False
    finally:
        conn.close()

def deleteuser(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''DROP USER %(user)s@%(ip)s''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while deleting user', RuntimeWarning)
        return False
    finally:
        conn.close()

def renameuser(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''RENAME USER %(user)s TO %(newuser)s''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while deleting user', RuntimeWarning)
        return False
    finally:
        conn.close()

def revokeuser(**opts):
    try:
        conn, curs = connect(opts['db'])
        permset = str()
        for eachtype in opts['perms']:
            permset += '%s,' % eachtype
        opts['perms'] = permset[:-1]
        curs.execute('''REVOKE %(perms)s ON %(db)s.%(table) FROM "%(user)s"@"%(ip)s"''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while deleting user', RuntimeWarning)
        return False
    finally:
        conn.close()

def setpasswduser(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''SET PASSWORD FOR "%(user)s"@"%(ip)s" = PASSWORD("%(newpasswd)s")''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while deleting user', RuntimeWarning)
        return False
    finally:
        conn.close()

def update(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''UPDATE %(db)s.%(table) SET %(key)s = %(value)s WHERE %(cond)s = %(exp)s''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while updating field', RuntimeWarning)
        return False
    finally:
        conn.close()

def report(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''SELECT %(column)s FROM %(db)s.%(table)s WHERE $(cond)s = %(exp)s''', **opts)
        return curs.fetchall()
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while reporting rows', RuntimeWarning)
        return False
    finally:
        conn.close()

def deleterow(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''DROP FROM %(db)s.%(table)s WHERE %(cond)s = %(exp)s''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while deleting row', RuntimeWarning)
        return False
    finally:
        conn.close()

def dropdb(**opts):
    try:
        conn, curs = connect()
        curs.execute('''DROP DATABASE %(db)s''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
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
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while creating db', RuntimeWarning)
        return False
    finally:
        conn.close()

def repairtable(**opts):
    try:
        conn, curs = connect(opts['db'])
        curs.execute('''REPAIR TABLE %(db)s.%(table)s''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while repairing table', RuntimeWarning)
        return False
    finally:
        conn.close()

def backuptable(**opts):
    try:
        conn, curs = connect(opts['db'])
        tableset = str()
        for table in opts['table']:
            tableset += '%s,' % table
        opts['table'] = tableset[:-1]
        curs.execute('''BACKUP TABLE %(db)s.%(table) TO %(dir)s''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while backing up table', RuntimeWarning)
        return False
    finally:
        conn.close()

def restoretable(**opts):
    try:
        conn, curs = connect(opts['db'])
        tableset = str()
        for table in opts['table']:
            tableset += '%s,' % table
        opts['table'] = tableset[:-1]
        curs.execute('''RESTORE TABLE %(db)s.%(table)s FROM %(dir)s''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while restoring table', RuntimeWarning)
        return False
    finally:
        conn.close()

def analyzetable(**opts):
    try:
        conn, curs = connect(opts['db'])
        for table in opts['table']:
            tableset += '%s,' % table
        opts['table'] = tableset[:-1]
        curs.execute('''ANALYZE TABLE %(db)s.%(table)s''', **opts)
        return curs.fetchall()
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while analyzing table', RuntimeWarning)
        return False
    finally:
        conn.close()

def optimizetable(**opts):
    try:
        conn, curs = connect(opts['db'])
        for table in opts['table']:
            tableset += '%s,' % table
        opts['table'] = tableset[:-1]
        curs.execute('''OPTIMIZE TABLE %(db)s.%(table)s''', **opts)
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while analyzing table', RuntimeWarning)
        return False
    finally:
        conn.close()

def checksumtable(**opts):
    try:
        conn, curs - connect(opts['db'])
        for table in opts['table']:
            tableset += '%s,' % table
        opts['table'] = tableset[:-1]
        curs.execute('''CHECKSUM TABLE %(table)s %(method)s''', **opts)
        return curs.fetchall()
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while analyzing table', RuntimeWarning)
        return False
    finally:
        conn.close()

def createtable(**opts):
    try:
        conn, curs = connect(opts['db'])
        query = str()
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
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error whilst creating table', RuntimeWarning)
        return False
    finally:
        conn.close()

def insert(**opts):
    try:
        '''
        opts = {'col': ['id', 'name'],
                'row': ['NULL', 'jimmy']}
        '''
        colset, rowset = str(), str()
        for eachCol, eachRow in zip(opts['col'], opts['row']):
            colset += '%s,' % eachCol
            rowset += '%s,' % eachRow
        opts['col'] = colset[:-1]
        opts['row'] = rowset[:-1]
        '''
        NOW
        opts = {'col': "id, name",
                'row': "NULL, jimmy"}
        '''
        conn, curs = connect(opts['db'])
        curs.execute('''INSERT INTO %(db)s.%(table)s (%(col)s) VALUES (%(row)s)''', **opts)
        return True
    except sql.Error as e:
        warn('mysql error: %s' % e.message, RuntimeWarning)
        return False
    except:
        warn('error while inserting into table', RuntimeWarning)
        return False
    finally:
        conn.close()
