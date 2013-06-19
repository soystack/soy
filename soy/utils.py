#!/usr/bin/env python

'''
soy utilities class for rendering files.
'''

from jinja2 import Template

def prepare(string, *args):
    '''
    write
    '''
    try:
        for item in args:
            filehandle = open(item, 'wr+')
            filehandle.write("%s" % string)
            filehandle.close()
        return True
    except (OSError, IOError):
        return False

def commit(tmpl, path, **kwargs):
    '''
    render
    '''
    try:
        include = Template(open(tmpl, 'r+').read())
        prepare(include.render(**kwargs), path)

        return True
    except Exception:
        raise Exception
