dovecot:
  pkg:
    - installed
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
