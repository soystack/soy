include:
  - postfix

dovecot:
  pkg:
    - installed
    - require:
      - file: /etc/postfixadmin/vacation.conf
  service:
    - running
    - enable: True
    - full_restart: True
    - watch:
      - file: dovecot
  file.managed:
    - name: /etc/dovecot/dovecot.conf
    - source: salt://dovecot/dovecot.conf
    - template: jinja
    - require:
      - pkg: dovecot

/etc/dovecot/dovecot.conf:
  file.managed:
    - source: salt://dovecot/dovecot.conf
    - template: jinja
    - require:
      - file: dovecot

/etc/dovecot/trash.conf:
  file.managed:
    - source: salt://dovecot/trash.conf
    - template: jinja
    - require:
      - file: /etc/dovecot/dovecot.conf

/etc/dovecot/dovecot-mysql.conf:
  file.managed:
    - source: salt://dovecot/dovecot-mysql.conf
    - template: jinja
    - require:
      - file: /etc/dovecot/trash.conf

/etc/dovecot/dovecot-dict-quota.conf:
  file.managed:
    - source: salt://dovecot/dovecot-dict-quota.conf
    - template: jinja
    - require:
      - file: /etc/dovecot/dovecot-mysql.conf

mk_sieve:
  cmd.run:
    - name: mkdir /home/sieve
    - require:
      - file: /etc/dovecot/dovecot-dict-quota.conf

/home/sieve/globalfilter.sieve:
  file.managed:
    - source: salt://dovecot/globalfilter.sieve
    - template: jinja
    - require:
      - cmd: mk_sieve

chown_sieve:
  cmd.run:
    - name: chown -R vmail:mail /home/sieve
    - require:
      - file: /home/sieve/globalfilter.sieve
