dep:
  pkg.installed:
    - pkgs:
      - nfs-utils
      - rpcbind
      - system-config-firewall-tui

/etc/sysconfig/selinux:
  file.managed:
    - source: salt://nfs-server/selinux
    - require:
      - pkg: dep

setenforce:
  cmd.run:
    - name: setenforce 0
    - require:
      - file: /etc/sysconfig/selinux

/nfsshare:
  file.directory:
    - name: /nfsshare
    - makedirs: True
    - require:
      - cmd: setenforce

nfs_on:
  service:
    - name: nfs
    - running
    - enable: True
    - require:
      - file: /nfsshare

nfslock_on:
  service:
    - name: nfslock
    - running
    - enable: True
    - require:
      - service: nfs_on

rpcbind_on:
  service:
    - name: rpcbind
    - running
    - enable: True
    - require:
      - service: nfslock_on

/etc/exports:
  file.append:
    - source: salt://nfs-server/exports
    - require:
      - service: rpcbind_on

/etc/hosts.allow:
  file.append:
    - source: salt://nfs-server/hosts.allow
    - watch:
      - file: /etc/exports

/etc/hosts.deny:
  file.append:
    - source: salt://nfs-server/hosts.deny
    - watch:
      - file: /etc/hosts.allow

rpcbind_restart:
  service.running:
    - name: rpcbind
    - full_restart: True
    - watch:
      - file: /etc/hosts.deny

nfs_restart:
  service.running:
    - name: nfs
    - full_restart: True
    - require:
      - service: rpcbind_restart

nfslock_restart:
  service.running:
    - name: nfslock
    - full_restart: True
    - require:
      - service: nfs_restart
