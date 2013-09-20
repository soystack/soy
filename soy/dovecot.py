#!/usr/bin/env python

import MySQLdb
from soy import mysql

class Mail:
    def __init__(self, **kwargs):
        self.mysql = mysql.Setup(__salt__, 'dovecot').mysql
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

        try:
            self.db = MySQLdb.connect(**self.mysql)
            self.curs = self.db.cursor()
        except:
            return None

    def forward(self):
        try:
            self.curs.execute("""INSERT INTO virtual_aliases
                                             (`id`,
                                              `domain_id`,
                                              `source`,
                                              `destination`)
                                 VALUES      (NULL,
                                              $(domain)s,
                                              $(source)s,
                                              $(destination)s)""", self)
            self.db.commit()
            return {'status': True}
        except:
            return {'status': False}

    def add_domain(self):
        try:
            self.curs.execute("""INSERT INTO virtual_domains
                                             (`id`,
                                              `name``)
                                 VALUES      (NULL,
                                              $(name)s)""", self)
            self.db.commit()
            return {'status': True}
        except:
            return {'status': False}

    def add_user(self):
        try:
            self.curs.execute("""INSERT INTO virtual_users
                                             (`id`,
                                              `domain_id`,
                                              `password`,
                                              `email`)
                                 VALUES      (NULL,
                                              $(domain_id)s,
                                              $(password)s,
                                              $(email)s)""", self)
            self.db.commit()
            return {'status': True}
        except:
            return {'status': False}
