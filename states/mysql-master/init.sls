include:
  - mysql

config:
  file.managed:
    - name: /etc/my.cnf
    - source: salt://mysql-master/my.cnf
    - template: jinja
    - require:
      - service: mysql_base

mysqld:
  service.running:
    - watch:
      - file: config
