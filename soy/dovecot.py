#!/usr/bin/env python

import MySQLdb
from soy import mysql

class Dovecot:
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
