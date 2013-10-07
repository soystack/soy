from flask import Flask, jsonify, render_template

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

@app.route('/dns/create/<name>/<master>/<last_check>/<d_type>/<not_srl>/<account>/<ttl>/<prio>/<d_id>')
def dnscreate(name, master, last_check, d_type, not_srl, account, ttl, prio, d_id):
    minion = 'powerdns.com'
    status = {}
    dopts = {'name': name,
             'master': master,
             'last_check': last_check,
             'type': d_type,
             'notified_serial': not_srl,
             'account': account}
    ropts = {'name': name,
             'ttl': ttl,
             'prio': prio,
             'last_check': last_check,
             'd_id': d_id}
    status['domain'] = c.cmd(minion, 'soy_pdns.createdomain', [**dopts])
    status['record'] = c.cmd(minion, 'soy_pdns.createrecord', [**ropts])
    return jsonify(status)

@app.route('/dns/report/domain')
def dnsreportdomain():
    minion = 'powerdns.localhost'
    status = {}
    report = c.cmd(minion, 'soy_pdns.reportdomain', [])
    for domain in report[minion]:
        status[domain['name']] = domain
    return jsonify(status)

@app.route('/dns/update/domain/<e_id>/<name>/<master>/<last_check>/<e_type>/<notified_serial>/<account>')
def dnsupdatedomain(name, e_id, e_type, account, last_check, notified_serial, master):
    minion = 'powerdns.localhost'
    opts = {'name': name,
            'id': e_id,
            'type': e_type,
            'account': account,
            'last_check': last_check,
            'notified_serial': notified_serial,
            'master': master}
    status = c.cmd(user, 'soy_pdns.updatedomain', [**opts])
    return jsonify(status)

@app.route('/dns/delete/domain/<e_id>')
def dnsdeletedomain(e_id):
    minion = 'powerdns.localhost'
    status = c.cmd(minion, 'soy_pdns.deletedomain', [e_id])
    return jsonify(status)

@app.route('/dns/report/record')
def dnsreportrecord():
    minion = 'powerdns.localhost'
    status = {}
    report = c.cmd(minion, 'soy_pdns.reportrecord', [])
    for domain in report[minion]:
        status[domain['id']] = domain
    return jsonify(status)

@app.route('/dns/update/record/<account>/<e_id>/<domain_id>/<name>/<e_type>/<content>/<ttl>/<prio>/<change_date>/<ordername>/<auth>')
def dnsupdaterecord(account, e_id, domain_id, name, e_type, content, ttl, prio, change_date, ordername, auth):
    minion = 'powerdns.localhost'
    opts = {'e_id':      e_id,      'domain_id':   domain_id, 'name': name,
            'e_type':    e_type,    'content':     content,   'ttl':  ttl,
            'prio':      prio,      'change_date': change_date,
            'ordername': ordername, 'auth':        auth}
    status = c.cmd(minion, 'soy_pdns.updaterecord', [**opts])
    return jsonify(status)

@app.route('/dns/delete/record/<e_id>')
def dnsdeleterecord(e_id):
    minion = 'powerdns.localhost'
    status = c.cmd(user, 'soy_pdns.deleterecord', [e_id])
    return jsonify(status)
