from flask import Flask, jsonify, render_template

'''
MYSQL (user)
'''

@app.route('/mysql/grant/<user>/<ip>/<db>/<table>/<path: perms>', methods=['POST'])
def mysqlgrant(user, ip, db, table, perms):
    minion = 'mysql_user.localdomain'
    opts = {'user': user, 'ip': ip, 'db': db,
            'table': table, 'perms': perms.rsplit('/')}
    return jsonify(c.cmd(minion, 'soy_user_mysql.grant', **opts))

@app.route('/mysql/adduser/<user>/<ip>/<passwd>/<db>/<table>', methods=['POST'])
def mysqladduser(user, ip, passwd, db, table):
    minion = 'mysql_user.localdomain'
    opts = {'user': user, 'ip': ip, 'passwd': passwd,
            'db': db, 'table': table}
    return jsonify(c.cmd(minion, 'soy_user_mysql.adduser', **opts))

@app.route('/mysql/createdb/<db>/<user>/<ip>', methods=['POST'])
def mysqlcreatedb(db, user, ip):
    minion = 'mysql_user.localdomain'
    opts = {'db': db, 'user': user, 'ip': ip}
    return jsonify(c.cmd(minion, 'soy_user_mysql.createdb', **opts))

@app.route('/mysql/createtable/<db>/<table>/<path: fields>', methods=['POST'])
def mysqlcreatetable(db, table, fields):
    '''
    fields = '/id:ID AUTO_INCREMENT/name:VARCHAR NOT NULL
    '''
    fieldopts = dict()
    for field in fields.rsplit('/')[1:]:
        fieldopts[field.rsplit(':')[0]] = field.rsplit(':')[1]
    minion = 'mysql_user.localdomain'
    opts = {'db': db, 'table': table, 'fields': opts}
    return jsonify(c.cmd(minion, 'soy_user_mysql.createtable', **opts))
