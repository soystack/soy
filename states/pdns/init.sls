include:
  - mysql-master
  - syslog

powerdns:
  pkg.installed:
    - pkgs:
      - pdns
      - pdns-backend-mysql
    - require:
      - service: mysqld

pdns:
  service:
    - running
    - full_restart: True
    - watch:
      - file: /etc/pdns/pdns.conf

/etc/schema:
  file.managed:
    - source: salt://pdns/schema
    - template: jinja
    - require:
      - service: mysqld

/etc/pdns/pdns.conf:
  file.managed:
    - source: salt://pdns/pdns.conf
    - template: jinja
    - require:
      - file: /etc/schema

mysql:
  mysql_database.present:
    - name: dns
    - require:
      - pkg: powerdns
      - cmd: setpass

loadschema:
  cmd.run:
    - name: mysql -u{{pillar['mysql.user']}} -p{{pillar['mysql.pass']}} dns < /etc/schema
    - require:
      - mysql_database: mysql
      - file: /etc/schema
