/etc/my.cnf:
  file.managed:
    - source: salt://mysql-slave/my.cnf
    - template: jinja
    - watch:
      - pkg: mysql
