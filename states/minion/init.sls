/etc/salt/minion:
  file.managed:
    - source: salt://minion/minion
    - template: jinja 
