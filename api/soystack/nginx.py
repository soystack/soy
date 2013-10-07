from flask import Flase, jsonify, render_template

'''
NGINX
'''

@app.route('/nginx/create/<user>/<host>', methods=['GET'])
def nginxcreate(user, host):
    minion = 'nginx.localdomain'
    return jsonify(c.cmd(minion, 'soy_nginx.create', [user, host]))

@app.route('/nginx/report/<user>', methods=['GET'])
def nginxreport(user):
    minion = 'nginx.localdomain'
    return jsonify(c.cmd(minion, 'soy_nginx.report', [user]))

@app.route('/nginx/update/<user>/<host>/<updated_host>', methods=['PUT'])
def nginxupdate(user, host, updated_host):
    minion = 'nginx.localdomain'
    return jsonify(c.cmd(minion, 'soy_nginx.update', [user, host, updated_host]))

@app.route('/nginx/delete/<user>/<host>', methods=['GET'])
def nginxdelete(user, host):
    minion = 'nginx.localdomain'
    return jsonify(c.cmd(user, 'soy_nginx.delete', [user, host]))

@app.route('/nginx/suspend/<user>/<host>', methods=['GET'])
def nginxsuspend(user, host):
    minion = 'nginx.localdomain'
    opts = {'user': user,
            'host': host}
    return jsonify(c.cmd(minion, 'soy_nginx.suspend', [**opts]))

@app.route('/nginx/unsuspend/<user>/<host>', methods=['GET'])
def nginxunsuspend(user, host):
    minion = 'nginx.localdomain'
    opts = {'user': user,
            'host': host}
    return jsonify(c.cmd(minion, 'soy_nginx.unsuspend', [**opts]))
