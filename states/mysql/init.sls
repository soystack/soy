mysql_base:
  pkg.installed:
    - pkgs:
      - mysql
      - mysql-server
      - MySQL-python
  service.running:
    - name: mysqld
    - enable: True
    - full_restart: True
    - require:
      - pkg: mysql_base

setpass:
  cmd.run:
    - name: mysqladmin -uroot password {{pillar['mysql.pass']}}
    - require:
      - service: mysql_base
