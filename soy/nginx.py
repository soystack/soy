#!/usr/bin/env python

'''
The following Host class provides several sane methods of interaction when         
dealing with nginx from a virtualhost perspective. This perspective includes       
user and administrative functionality. Some of these methods include create,       
delete, suspend, and resume.
'''

import soy.utils as soy


class Host(object):
    '''
    initalize Host class
    '''
    def __init__(self, __salt__, **kwargs):
        self.salt = __salt__
        self.pillar = self.salt['pillar.raw']('nginx')
        for key, value in **kwargs:
            self.[key] = value

    def mkconf(self):
        '''
        write and symlink nginx host files from jinja2 template.
        '''
        try:
            available = '%s%s.conf' % (self.pillar['available'], self.host)
            enabled = '%s%s.conf' % (self.pillar['enabled'], self.host)
            soy.commit(self.pillar['template'], available, **self.__dict__)
            self.salt['file.symlink'](available, enabled)
            return True
        except (OSError, IOError):
            return False

    def mksource(self, htdocs):
        '''
        write source html template (placeholder, not required)
        '''
        try:
            path = '%s%s' % (htdocs, self.pillar['indexhtml'])
            soy.commit(self.pillar['index'], path, **self.__dict__)
            self.salt['nginx.signal']('reload')
            return True
        except (OSError, IOError):
            raise OSError

    def mkdir(self, htdocs):
        '''
        create host htdocs directory
        '''
        try:
            self.salt['file.mkdir'](htdocs)
            if self.pillar['index']:
                self.mksource(htdocs)
            return True
        except (OSError, IOError):
            return False

    def mklog(self, logdir):
        '''
        write log files in specified log directory
        '''
        try:
            self.salt['file.mkdir'](logdir)
            access = '%s%s' % (logdir, self.pillar['access'])
            error = '%s%s' % (logdir, self.pillar['error'])
            soy.prepare(None, access, error)
            return True
        except (OSError, IOError):
            return False

    def delete(self, user=False):
        '''
        delete entire file tree for host and or user 
        '''
        try:
            enabled = '%s%s.conf' % (self.pillar['enabled'], self.host)
            available = '%s%s.conf' % (self.pillar['available'], self.host)
            base = '%s%s/' % (self.pillar['base'], self.user)

            if user is True:
                self.salt['file.remove']('%S%S' % base, user)
            else:
                self.salt['file.remove'](available)
                self.salt['file.remove'](enabled)
                self.salt['file.remove']('%s%s' % (base, self.host))

            self.salt['nginx.signal']('reload')
            return True
        except (OSError, IOError, KeyError):
            return False

    def create(self):
        '''
        build host tree for new hosts
        '''
        root = '%s%s/%s' % (self.pillar['base'],
                            self.user,
                            self.host)
        htdocs = '%s%s' % (root, self.pillar['htdocs'])
        logdir = '%s%s' % (root, self.pillar['logs'])

        try:
            self.mkdir(htdocs)
            self.mklog(logdir)
            self.mkconf()
            self.salt['nginx.signal']('reload')
            return True
        except (OSError, IOError, KeyError, AttributeError):
            return self.delete()

    def suspend(self, user=False):
        '''
        suspend hosts 
        '''
        try:
            path = '%s%s.conf' % (self.pillar['available'], self.host)
            link = '%s%s.conf' % (self.pillar['enabled'], self.host)
            self.salt['file.remove'](link)
            self.salt['file.remove'](path)
            soy.commit(self.pillar['susconf'], path, **self.__dict__)
            self.salt['file.symlink'](path, link)
            self.salt['nginx.signal']('reload')
            return True
        except (OSError, IOError):
            return False

    def resume(self):
        '''
        resume normal operations on hosts that have been suspended
        '''
        try:
            path = '%s%s.conf' % (self.pillar['available'], self.host)
            link = '%s%s.conf' % (self.pillar['enabled'], self.host)
            self.salt['file.remove'](link)
            self.salt['file.remove'](path)
            self.mkconf()
            self.salt['nginx.signal']('reload')
            return True
        except (OSError, IOError):
            return False
