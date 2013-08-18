from flask import Flask, jsonify, render_template
from gevent.wsgi import WSGIServer
from salt.client import LocalClient

c    = LocalClient()
app  = Flask(__name__)

'''
Can't use the word 'domains' for placeholders??
'''

'''
NGINX
'''

@app.route('/nginx/create/<user>/<host>', methods=['GET'])
def nginxcreate(user, host):
	user = 'nginx.localdomain'
	opts = {'user': user,
			'host': host}
	return jsonify(c.cmd(user, 'soy_nginx.create', **opts)

@app.route('/nginx/report', methods=['GET'])
def nginxreport():
	user = 'nginx.localdomain'
	return jsonify(c.cmd(user, 'soy_nginx.report', [])

@app.route('/nginx/delete/<host>', methods=['GET'], defaults={'user': False})
@app.route('/nginx/delete/<host>/<user>')
def nginxdelete(user, host):
	user = 'nginx.localdomain'
	opts = {'user': user,
			'host': host}
	return jsonify(c.cmd(user, 'soy_nginx.delete', **opts)

@app.route('/nginx/suspend/<host>', methods=['GET'])
def nginxsuspend(host):
	user = 'nginx.localdomain'
	opts = {'host': host}
	return jsonify(c.cmd(user, 'soy_nginx.suspend', **opts)

@app.route('/nginx/unsuspend/<host>', methods=['GET'])
def nginxunsuspend(host):
	user = 'nginx.localdomain'
	opts = {'host': host}
	return jsonify(c.cmd(user, 'soy_nginx.unsuspend', **opts)

'''
DNS
'''

@app.route('/dns', methods=['GET'])
def dns():
	return render_template('dns.html')

@app.route('/dns/domain')
def dnsdomain():
	return render_template('domains.html')

@app.route('/dns/record')
def dnsrecord():
	return render_template('records.html')

@app.route('/dns/create/domain/<name>')
def dnscreate(name):
	user = 'powerdns.com'
	status = {}
	status['domain'] = c.cmd(user, 'soy_pdns.createDomain', [name])
	status['record'] = c.cmd(user, 'soy_pdns.createRecord', [name])
	return jsonify(status)

@app.route('/dns/report/domain')
def dnsreportdomain():
	user = 'powerdns.com'
	status = {}
	report = c.cmd(user, 'soy_pdns.reportDomain')
	for domain in report[user]:
		status[domain['name']] = domain
	return jsonify(status)

@app.route('/dns/update/domain/<id>/<name>/<master>/<last_check>/<type>/<notified_serial>/<account>')
def dnsupdatedomain(name, id, type, account, last_check, notified_serial, master):
	user = 'powerdns.com'
	kwargs = {'name':name,
			  'id':id,
			  'type':type,
			  'account':account,
			  'last_check':last_check,
			  'notified_serial':notified_serial,
			  'master':master}
	status = c.cmd(user, 'soy_pdns.updateDomain', **kwargs)
	return jsonify(status)

@app.route('/dns/delete/domain/<id>')
def dnsdeletedomain(id):
	user = 'powerdns.com'
	status = c.cmd(user, 'soy_pdns.deleteDomain', [id])
	return jsonify(status)

@app.route('/dns/report/record')
def dnsreportrecord():
	user = 'powerdns.com'
	status = {}
	report = c.cmd(user, 'soy_pdns.reportRecord')
	for domain in report[user]:
		status[domain['id']] = domain
	return jsonify(status)

@app.route('/dns/update/record/<name>/<id>/<master>/<last_check>/<type>/<notified_serial>/<account>')
def dnsupdaterecord(name, id, master, last_check, type, notified_serial, account):
	user = 'powerdns.com'
	kwargs = {'name':name,
			  'id': id,
			  'master':master,
			  'last_check':last_check,
			  'type':type,
			  'notified_serial':notified_serial,
			  'account':account}
	status = c.cmd(user, 'soy_pdns.updateRecord', **kwargs)
	return jsonify(status)

@app.route('/dns/delete/record/<id>')
def dnsdeleterecord(id):
	user = 'powerdns.com'
	status = c.cmd(user, 'soy_pdns.deleteRecord', [id])
	return jsonify(status)


if __name__ == '__main__':
	server = WSGIServer(('',80),app)
	server.serve_forever()
