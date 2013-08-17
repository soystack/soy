nginx:
  pkg:
    - installed
  service:
    - running
    - enable: True
    - require:
      - pkg: nginx

sites-available:
  file.directory:
    - name: /etc/nginx/sites-available
    - makedirs: True
    - require:
      - service: nginx

sites-enabled:
  file.directory:
    - name: /etc/nginx/sites-enabled
    - makedirs: True
    - require:
      - file: sites-available

/etc/nginx/nginx.conf:
  file.managed:
    - sources: salt://nginx/nginx.conf
    - template: jinja
    - mode: 660
    - require:
      - file: sites-enabled

/etc/nginx/virtualhost.conf.tpl:
  file.managed: 
    - source: salt://nginx/virtualhost.conf.tpl
    - mode: 660
    - require:
      - file: /etc/nginx/nginx.conf

/etc/nginx/index.html.tpl:
  file.managed:
    - source: salt://nginx/index.html.tpl
    - mode: 660
    - require:
      - file: /etc/nginx/virtualhost.conf.tpl
