include:
  - postfix-mysql

postfix:
  pkg:
    - installed
    - require:
      - cmd: load_schema
  service:
    - running
    - enable: True
    - full_restart: True
    - watch:
      - file: postfix
  file.managed:
    - name: /etc/postfix/main.cf
    - source: salt://postfix/main.cf
    - template: jinja
    - require:
      - pkg: postfix

/etc/postfix/master.cf:
  file.managed:
    - source: salt://postfix/master.cf
    - template: jinja
    - require:
      - file: postfix

/etc/postfix/mysql-domains.cf:
  file.managed:
    - source: salt://postfix/mysql-domains.cf
    - template: jinja
    - require:
      - file: /etc/postfix/master.cf

/etc/postfix/mysql-forwards.cf:
  file.managed:
    - source: salt://postfix/mysql-forwards.cf
    - template: jinja
    - require:
      - file: /etc/postfix/mysql-domains.cf

/etc/postfix/mysql-mailboxes.cf:
  file.managed:
    - source: salt://postfix/mysql-mailboxes.cf
    - template: jinja
    - require:
      - file: /etc/postfix/mysql-forwards.cf

/etc/postfix/mysql-email.cf:
  file.managed:
    - source: salt://postfix/mysql-email.cf
    - template: jinja
    - require:
      - file: /etc/postfix/mysql-mailboxes.cf

set_permissions:
  cmd.run:
    - name: chmod o= /etc/postfix/mysql-*
    - require:
      - file: /etc/postfix/mysql-email.cf

change_ownership:
  cmd.run:
    - name: chgrp {{ pillar['postfix']['specified_group'] }} /etc/postfix/mysql-*
    - require:
      - cmd: set_permissions
