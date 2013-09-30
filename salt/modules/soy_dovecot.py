#!/usr/bin/env python

import MySQLdb

def loadmysql():
    return __salt__['soy_mysql.setup']('dovecot')

def connect():
    try:
        mysql = loadmysql()
        db = MySQLdb.connect(**mysql)
        curs = db.cursor()
        return db, curs
    except:
        return None

def forward(**opts):
    try:
        db, curs = connect()
        curs.execute("""INSERT INTO virtual_aliases
                                     (`id`,
                                      `domain_id`,
                                      `source`,
                                      `destination`)
                         VALUES      (NULL,
                                      $(domain)s,
                                      $(source)s,
                                      $(destination)s)""", **opts)
        db.commit()
        return {'status': True}
    except:
        return {'status': False}

def add_domain(name):
    try:
        db, curs = connect()
        curs.execute("""INSERT INTO virtual_domains
                                     (`id`,
                                      `name``)
                        VALUES       (NULL,
                                      %s)""", (name,))
        db.commit()
        return {'status': True}
    except:
        return {'status': False}

def add_user(**opts):
    try:
        db, curs = connect()
        curs.execute("""INSERT INTO virtual_users
                                     (`id`,
                                      `domain_id`,
                                      `password`,
                                      `email`)
                        VALUES       (NULL,
                                      $(domain_id)s,
                                      $(password)s,
                                      $(email)s)""", **opts)
        db.commit()
        return {'status': True}
    except:
        return {'status': False}
