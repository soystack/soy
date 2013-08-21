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
def dnscreatedomain(name):
	user = 'powerdns.com'
	status = {}
	kwargs = {'name': name, 'func': 'create'}
	status['domain'] = c.cmd(user, 'soy_pdns.start_domain', [kwargs])
	status['record'] = c.cmd(user, 'soy_pdns.start_record', [kwargs])
	return jsonify(status)

@app.route('/dns/report/domain')
def dnsreportdomain():
	user = 'powerdns.com'
	status = {}
	kwargs = {'func': 'report'}
	report = c.cmd(user, 'soy_pdns.report_domain', [kwargs])
	for domain in report[user]:
		status[domain['name']] = domain
	return jsonify(status)

@app.route('/dns/update/domain/<e_id>/<name>/<master>/<last_check>/<e_type>/<notified_serial>/<account>')
def dnsupdatedomain(name, e_id, e_type, account, last_check, notified_serial, master):
	user = 'powerdns.com'
	kwargs = {'func':'update',
			  'name':name,
			  'e_id':e_id,
			  'e_type':e_type,
			  'account':account,
			  'last_check':last_check,
			  'notified_serial':notified_serial,
			  'master':master}
	status = c.cmd(user, 'soy_pdns.updateDomain', [kwargs])
	return jsonify(status)

@app.route('/dns/delete/domain/<e_id>')
def dnsdeletedomain(e_id):
	user = 'powerdns.com'
	kwargs = {'func': 'delete', 'e_id': e_id}
	status = c.cmd(user, 'soy_pdns.deleteDomain', [kwargs])
	return jsonify(status)

@app.route('/dns/report/record')
def dnsreportrecord():
	user = 'powerdns.com'
	status = {}
	kwargs = {'func':'report'}
	report = c.cmd(user, 'soy_pdns.reportRecord', [kwargs])
	for domain in report[user]:
		status[domain['id']] = domain
	return jsonify(status)

@app.route('/dns/update/record/<name>/<e_id>/<master>/<last_check>/<e_type>/<notified_serial>/<account>')
def dnsupdaterecord(name, e_id, master, last_check, e_type, notified_serial, account):
	user = 'powerdns.com'
	kwargs = {'func':'update',
			  'name':name,
			  'e_id': e_id,
			  'master':master,
			  'last_check':last_check,
			  'e_type':e_type,
			  'notified_serial':notified_serial,
			  'account':account}
	status = c.cmd(user, 'soy_pdns.updateRecord', [kwargs])
	return jsonify(status)

@app.route('/dns/delete/record/<e_id>')
def dnsdeleterecord(e_id):
	user = 'powerdns.com'
	kwargs = {'func': 'delete', 'e_id':e_id}
	status = c.cmd(user, 'soy_pdns.deleteRecord', [kwargs])
	return jsonify(status)


@app.route('/ftp/create/<user>/<pswd>')
def ftpcreate(user, pswd):
	user = 'vsftp.localdomain'
	kwargs = {'user': user,
			  'pswd': pswd}
	return jsonify(c.cmd(user, 'soy_vsftp.create', [kwargs]))

@app.route('/ftp/report')
def ftpreport():
	user = 'vsftp.localdomain'
	kwargs = {}
	return jsonify(c.cmd(user, 'soy_vsftp.report', [kwargs]))

@app.route('/ftp/update/<user>/<newuser>/<newpswd>')
def ftpupdate(user, newuser, newpswd):
	user = 'vsftp.localdomain'
	kwargs = {'user': user,
			  'newuser': newuser,
			  'newpswd': newpswd}
	return jsonify(c.cmd(user, 'soy_vsftp.update', [kwargs]))

@app.route('/ftp/delete/<user>')
def ftpdelete(user):
	user = 'vsftp.localdomain'
	kwargs = {'user': user}
	return jsonify(c.cmd(user, 'soy_vsftp.delete', [kwargs]))

if __name__ == '__main__':
	server = WSGIServer(('',80),app)
	server.serve_forever()
