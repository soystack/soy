#!/usr/bin/env python

from soy.nginx import Host

def report():
    return __salt__['pillar.raw']('nginx')

def create(**kwargs):
    return Host(__salt__, **kwargs).create()

def delete(**kwargs):
	return Host(__salt__, **kwargs).delete()

def suspend(**kwargs):
	return Host(__salt__, **kwargs).suspend()

def unsuspend(**kwargs):
    return Host(__salt__, **kwargs).unsuspend()
