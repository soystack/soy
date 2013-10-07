from flask import Flask, jsonify, render_template
from soystack
from gevent.wsgi import WSGIServer
from salt.client import LocalClient

c    = LocalClient()
app  = Flask(__name__)

if __name__ == '__main__':
    server = WSGIServer(('',80),app)
    server.serve_forever()
