nginx:
  available: '/etc/nginx/sites-available/'
  enabled: '/etc/nginx/sites-enabled/'
  template: '/etc/nginx/virtualhost.conf.tpl'
  susconf: '/etc/nginx/suspended.conf.tpl'
  sushtml: '/etc/nginx/suspended.html.tpl'
  sushtdocs: '/var/www/suspended/htdocs/index.html'
  index: '/etc/nginx/index.html.tpl'
  base: '/var/www/'
  htdocs: '/htdocs/'
  logs: '/logs/'
