#!/usr/bin/env python

from soy.nginx import Host

def report():
    return __salt__['pillar.raw']('nginx')

def create(**kwargs):
    ret = Host(__salt__,**kwargs)
    return ret.create()

def delete(**kwargs):
    ret = Host(__salt__, **kwargs)
    return ret.delete(user=False)

def suspend(**kwargs):
    ret = Host(__salt__, **kwargs)
    return ret.suspend()

def unsuspend(**kwargs):
    ret = Host(__salt__, **kwargs)
    return ret.unsuspend()
