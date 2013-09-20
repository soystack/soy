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
    return jsonify(c.cmd(user, 'soy_router.route', ['nginx', 'Host', 'create', opts])

@app.route('/nginx/report', methods=['GET'])
def nginxreport():
    user = 'nginx.localdomain'
    return jsonify(c.cmd(user, 'soy_router.route', ['nginx', 'Host', 'report', {}])

@app.route('/nginx/update/<host>/<updated_host>', methods=['PUT'])
def nginxupdate(host, updated_host):
    user = 'nginx.localdomain'
    opts = {'host': host,
        'updated_host': updated_host}
    return jsonify(user, 'soy_router.route', ['nginx','Host', 'update', opts])

@app.route('/nginx/delete/<host>', methods=['GET'], defaults={'user': False})
@app.route('/nginx/delete/<host>/<user>')
def nginxdelete(user, host):
    user = 'nginx.localdomain'
    opts = {'user': user,
            'host': host}
    return jsonify(c.cmd(user, 'soy_router.route', ['nginx', 'Host', 'delete', opts])

@app.route('/nginx/suspend/<host>', methods=['GET'])
def nginxsuspend(host):
    user = 'nginx.localdomain'
    opts = {'host': host}
    return jsonify(c.cmd(user, 'soy_router.route', ['nginx', 'Host', 'suspend', opts])

@app.route('/nginx/unsuspend/<host>', methods=['GET'])
def nginxunsuspend(host):
    user = 'nginx.localdomain'
    opts = {'host': host}
    return jsonify(c.cmd(user, 'soy_router.route', ['nginx', 'Host', 'unsuspend', opts])

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

@app.route('/dns/create/<name>')
def dnscreate(name):
    user = 'powerdns.com'
    status = {}
    kwargs = {'name': name}
    status['domain'] = c.cmd(user, 'soy_router.route', ['pdns', 'Domain', 'create', kwargs])
    status['record'] = c.cmd(user, 'soy_router.route', ['pdns', 'Record', 'create', kwargs])
    return jsonify(status)

@app.route('/dns/report/domain')
def dnsreportdomain():
    user = 'powerdns.com'
    kwargs, status = {}, {}
    report = c.cmd(user, 'soy_router.route', ['pdns', 'Domain', 'report', kwargs])
    for domain in report[user]:
        status[domain['name']] = domain
    return jsonify(status)

@app.route('/dns/update/domain/<e_id>/<name>/<master>/<last_check>/<e_type>/<notified_serial>/<account>')
def dnsupdatedomain(name, e_id, e_type, account, last_check, notified_serial, master):
    user = 'powerdns.com'
    kwargs = {'name':name,
              'e_id':e_id,
              'e_type':e_type,
              'account':account,
              'last_check':last_check,
              'notified_serial':notified_serial,
              'master':master}
    status = c.cmd(user, 'soy_router.route', ['pdns', 'Domain', 'update', kwargs])
    return jsonify(status)

@app.route('/dns/delete/domain/<e_id>')
def dnsdeletedomain(e_id):
    user = 'powerdns.com'
    kwargs = {'e_id': e_id}
    status = c.cmd(user, 'soy_router.route', ['pdns', 'Domain', 'delete', kwargs])
    return jsonify(status)

@app.route('/dns/report/record')
def dnsreportrecord():
    user = 'powerdns.com'
    status = {}
    kwargs = {}
    report = c.cmd(user, 'soy_router.route', ['pdns', 'Record', 'report', kwargs])
    for domain in report[user]:
        status[domain['id']] = domain
    return jsonify(status)

@app.route('/dns/update/record/<e_id>/<domain_id>/<name>/<e_type>/<content>/<ttl>/<prio>/<change_date>/<ordername>/<auth>')
def dnsupdaterecord(e_id, domain_id, name, e_type, content, ttl, prio, change_date, ordername, auth):
    user = 'powerdns.com'
    kwargs = {'e_id':      e_id,      'domain_id':   domain_id, 'name': name,
              'e_type':    e_type,    'content':     content,   'ttl':  ttl,
              'prio':      prio,      'change_date': change_date,
              'ordername': ordername, 'auth':        auth}
    status = c.cmd(user, 'soy_router.route', ['pdns', 'Record', 'update', kwargs])
    return jsonify(status)

@app.route('/dns/delete/record/<e_id>')
def dnsdeleterecord(e_id):
    user = 'powerdns.com'
    kwargs = {'e_id':e_id}
    status = c.cmd(user, 'soy_router.route', ['pdns', 'Record', 'delete', kwargs])
    return jsonify(status)

'''
FTP
'''

@app.route('/ftp/create/<user>/<pswd>')
def ftpcreate(user, pswd):
    user = 'vsftp.localdomain'
    kwargs = {'user': user,
              'pswd': pswd}
    return jsonify(c.cmd(user, 'soy_router.route', ['vsftp', 'User', 'create', kwargs]))

@app.route('/ftp/report')
def ftpreport():
    user = 'vsftp.localdomain'
    kwargs = {}
    return jsonify(c.cmd(user, 'soy_router.route', ['vsftp', 'User', 'report', kwargs]))

@app.route('/ftp/update/<user>/<newuser>/<newpswd>')
def ftpupdate(user, newuser, newpswd):
    user = 'vsftp.localdomain'
    kwargs = {'user': user,
              'newuser': newuser,
              'newpswd': newpswd}
    return jsonify(c.cmd(user, 'soy_router.route', ['vsftp', 'User', 'update', kwargs]))

@app.route('/ftp/delete/<user>')
def ftpdelete(user):
    user = 'vsftp.localdomain'
    kwargs = {'user': user}
    return jsonify(c.cmd(user, 'soy_router.route', ['vsftp', 'User', 'delete', kwargs]))

'''
MAIL
'''

@app.route('/mail/forward/<domain>/<source>/<dest>', methods=['POST'])
def mailforward(self, domain, source, dest):
    user = 'mail.localdomain'
    kwargs = {'domain': domain,
              'source': source,
              'destination': dest}
    return jsonify(c.cmd(user, 'soy_router.route', ['dovecot', 'Mail', 'forward', kwargs]))

@app.route('/mail/adddomain/<name>', methods=['POST'])
def mailadddomain(self, name):
    user = 'mail.localdomain'
    kwargs = {'name': name}
    return jsonify(c.cmd(user, 'soy_router.route', ['dovecot', 'Mail', 'add_domain', kwargs]))

@app.route('/mail/adduser/<domainid>/<password>/<email>', methods=['POST'])
def adduser(self):
    user= 'mail.localdomain'
    kwargs = {'domain_id': domainid,
              'password': password,
              'email': email}
    return jsonify(c.cmd(user, 'soy_router.route', ['dovecot', 'Mail', 'add_user', kwargs]))

if __name__ == '__main__':
    server = WSGIServer(('',80),app)
    server.serve_forever()
