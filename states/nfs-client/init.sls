dep:
  pkg.installed:
    - pkgs:
      - nfs-utils
      - rpcbind

/etc/sysconfig/selinux:
  file.managed:
    - source: salt://nfs-client/selinux
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

nfs:
  service.running:
    - name: nfs
    - enable: True
    - full_restart: True
    - require:
      - file: /nfsshare

nfslock:
  service.running:
    - name: nfslock
    - enable: True
    - full_restart: True
    - require:
      - service: nfs

rpcbind:
  service.running:
    - name: rpcbind
    - enable: True
    - full_restart: True
    - require:
      - service: nfslock
