from flask import Flask, jsonify, render_template

'''
FTP
'''

@app.route('/ftp/create/<user>/<pswd>')
def ftpcreate(user, pswd):
    minion = 'vsftp.localdomain'
    return jsonify(c.cmd(minion, 'soy_vsftp.create', [user, pswd]))

@app.route('/ftp/report')
def ftpreport():
    minion = 'vsftp.localdomain'
    return jsonify(c.cmd(minion, 'soy_vsftp.report', []))

@app.route('/ftp/update/<user>/<newuser>/<newpswd>')
def ftpupdate(user, newuser, newpswd):
    minion = 'vsftp.localdomain'
    return jsonify(c.cmd(minion, 'soy_vsftp.update', [user, newuser, newpswd]))

@app.route('/ftp/delete/<user>')
def ftpdelete(user):
    minion = 'vsftp.localdomain'
    return jsonify(c.cmd(minion, 'soy_vsftp.delete', [user]))
