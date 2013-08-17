mysql_base:
  pkg.installed:
    - pkgs:
      - mysql
      - mysql-server
      - MySQL-python
    - watch_in:
      - service: mysql_base
  service.running:
    - name: mysqld
    - enable: True
    - full_restart: True
    - require_in:
      - cmd: setpass

setpass:
  cmd.run:
    - name: mysqladmin -uroot password {{pillar['mysql.pass']}}
