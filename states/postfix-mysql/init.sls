{% set pass = pillar['mysql.pass'] %}

include:
  - mysql

mailadmin:
  mysql_user.present:
    - host: localhost
    - require:
      - cmd: setpass

mailadmin_pass:
  cmd.run:
    - name: mysql -uroot -p{{pass}} -e 'update mysql.user set password=PASSWORD("{{pass}}") where User="mailadmin"'
    - require:
      - mysql_user: mailadmin

mailadmin_grants:
  mysql_grants.present:
    - grant: all privileges
    - database: mail.*
    - user: mailadmin
    - require:
      - cmd: mailadmin_pass

mailadmin_schema_perms:
  cmd.run:
    - name: mysql -uroot -p{{pass}} -e 'GRANT RELOAD, FILE ON *.* TO "mailadmin"@"localhost"'
    - require:
      - mysql_grants: mailadmin_grants

flush_privileges:
  cmd.run:
    - name: mysql -uroot -p{{pass}} -e 'flush privileges'
    - require:
      - cmd: mailadmin_schema_perms

/etc/schema:
  file.managed:
    - source: salt://postfix-mysql/schema
    - template: jinja
    - require:
      - cmd: flush_privileges

create_database:
  mysql_database.present:
    - name: mail
    - require:
      - file: /etc/schema

load_schema:
  cmd.run:
    - name: mysql -uroot -p{{pillar['mysql.pass']}} mail < /etc/schema
    - require:
      - mysql_database: create_database
