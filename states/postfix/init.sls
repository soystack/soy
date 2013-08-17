postfix:
  pkg:
    - installed
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
