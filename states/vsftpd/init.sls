include:
  - db4

vsftpd:
  pkg.installed:
    - pkgs:
      - vsftpd
      - ftp
    - require:
      - pkg: db4
  file.managed:
    - name: /etc/vsftpd/vsftpd.conf
    - source: salt://vsftpd/vsftpd.conf
    - template: jinja
    - require:
      - pkg: vsftpd
  service:
    - running
    - enable: True
    - full_restart: True
    - watch:
      - cmd: install_lib

magic_touch:
  cmd.run:
    - name: setsebool -P ftp_home_dir on && touch /etc/vsftpd/user_list
    - require:
      - service: vsftpd

/etc/vsftpd/vusers.txt:
  file.managed:
    - source: salt://vsftpd/vusers.txt
    - require:
      - cmd: magic_touch

load_users:
  cmd.run:
    - name: db_load -T -t hash -f /etc/vsftpd/vusers.txt /etc/vsftpd/vsftpd-virtual-user.db && rm -f /etc/vsftpd/vusers.txt
    - require:
      - file: /etc/vsftpd/vusers.txt

/etc/vsftpd/vsftpd-virtual-user.db:
  file.managed:
    - mode: 600
    - require:
      - cmd: load_users

/etc/pam.d/vsftpd.virtual:
  file.managed:
    - source: salt://vsftpd/vsftpd.virtual
    - require:
      - file: /etc/vsftpd/vsftpd-virtual-user.db

/home/vftp:
  file.directory:
    - makedirs: True
    - require:
      - file: /etc/pam.d/vsftpd.virtual

#the rest is totally custom to fit the example
make_home:
  cmd.run:
    - name: mkdir -p /home/vftp/jbert
    - require:
      - file: /home/vftp

change_perms:
  cmd.run:
    - name: chown -R ftp:ftp /home/vftp
    - require:
      - cmd: make_home
