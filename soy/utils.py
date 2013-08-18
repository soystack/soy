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
            filehandle = open(item, 'w+')
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
        include = Template(open(tmpl, 'w+').read())
        render = include.render(**kwargs)
        filehandle = open(path, 'w+')
        filehandle.write("%s" % render)
        filehandle.close()
        return True
    except (OSError, IOError):
        return False

def contains_all(arg, kwargs):
	'''
	checks kwargs for keys in arg
	'''
	res = []
	for e in arg:
		if e not in kwargs.keys():
			res.append(False)

	if False in res:
		return False
	return True
