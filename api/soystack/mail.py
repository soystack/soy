from flask import Flask, jsonify, render_template

'''
MAIL
'''

@app.route('/mail/forward/<domain>/<source>/<dest>', methods=['POST'])
def mailforward(domain, source, dest):
    minion = 'mail.localdomain'
    opts = {'domain': domain,
            'source': source,
            'destination': dest}
    return jsonify(c.cmd(minion, 'soy_dovecot.forward', [**opts]))

@app.route('/mail/adddomain/<name>', methods=['POST'])
def mailadddomain(name):
    minion = 'mail.localdomain'
    return jsonify(c.cmd(minion, 'soy_dovecot.add_domain', [name]))

@app.route('/mail/adduser/<domainid>/<password>/<email>', methods=['POST'])
def mailadduser(domainid, password, email):
    minion = 'mail.localdomain'
    opts = {'domain_id': domainid,
            'password': password,
            'email': email}
    return jsonify(c.cmd(minion, 'soy_dovecot.add_user', [**opts]))
