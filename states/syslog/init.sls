/etc/audisp/plugins.d/syslog.conf:
  file.managed:
    - source: salt://syslog/syslog.conf
    - template: jinja  
  service.running:
    - name: rsyslog
    - full_restart: True
    - watch:
      - file: /etc/audisp/plugins.d/syslog.conf
