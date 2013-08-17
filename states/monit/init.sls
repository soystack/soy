monit:
  pkg.installed:
    - name: monit
  service:
    - running
    - enable: True
    - full_restart: True
    - watch:
        - file: /etc/monit.conf

/etc/monit.conf:
  file.managed:
    - source: salt://monit/monit.conf
    - template: jinja
    - mode: 700
    - require:
      - pkg: monit
