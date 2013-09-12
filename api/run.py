#!/usr/bin/env python

from eve import Eve
from salt.router import route

app = Eve()
app.run()

# something like this
def nginx_create(request, payload):
  return route('nginx', 'Host', 'create', request)

app.on_GET_nginx_create += nginx_create
