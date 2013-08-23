include:
  - postfixadmin

postfix:
  pkg:
    - installed
    - require:
      - cmd: mv_postfixadmin
  service:
    - running
    - enable: True
    - full_restart: True
    - watch:
      - file: postfix
  file.managed:
    - name: /etc/postfix/main.cf
    - source: salt://postfix/main.cf
    - template: jinja
    - require:
      - pkg: postfix

/etc/postfix/master.cf:
  file.managed:
    - source: salt://postfix/master.cf
    - template: jinja
    - require:
      - file: postfix

/etc/postfix/mynetworks:
  file.managed:
    - source: salt://postfix/mynetworks
    - template: jinja
    - require:
      - file: /etc/postfix/master.cf

/etc/postfix/mysql-virtual_alias_maps.cf:
  file.managed:
    - source: salt://postfix/mysql-virtual_alias_maps.cf
    - template: jinja
    - require:
      - file: /etc/postfix/mynetworks

/etc/postfix/mysql-virtual_domains_maps.cf:
  file.managed:
    - source: salt://postfix/mysql-virtual_domains_maps.cf
    - template: jinja
    - require:
      - file: /etc/postfix/mysql-virtual_alias_maps.cf

/etc/postfix/mysql-relay_domains_maps.cf:
  file.managed:
    - source: salt://postfix/mysql-relay_domains_maps.cf
    - template: jinja
    - require:
      - file: /etc/postfix/mysql-virtual_domains_maps.cf

/etc/postfix/mysql-virtual_mailbox_maps.cf:
  file.managed:
    - source: salt://postfix/mysql-virtual_mailbox_maps.cf
    - template: jinja
    - require:
      - file: /etc/postfix/mysql-relay_domains_maps.cf

/etc/postfix/mysql-virtual_mailbox_limit_maps.cf:
  file.managed:
    - source: salt://postfix/mysql-virtual_mailbox_limit_maps.cf
    - template: jinja
    - require:
      - file: /etc/postfix/mysql-virtual_mailbox_maps.cf

touch_virt_regex:
  cmd.run:
    - name: touch /etc/postfix/virtual_regexp
    - require:
      - file: /etc/postfix/mysql-virtual_mailbox_limit_maps.cf

add_vacation:
  cmd.run:
    - name: useradd -r -d /var/spool/vacation -s /sbin/nologin -c "Virtual vacation" vacation
    - require:
      - cmd: touch_virt_regex

mk_vacation_dir:
  cmd.run:
    - name: mkdir /var/spool/vacation
    - require:
      - cmd: add_vacation

chmod_vacation:
  cmd.run:
    - name: chmod 770 /var/spool/vacation
    - require:
      - cmd: mk_vacation_dir

cp_vacation:
  cmd.run:
    - name: cp /usr/share/postfixadmin/VIRTUAL_VACATION/vacation.pl /var/spool/vacation/
    - require:
      - cmd: chmod_vacation

echo_transport:
  cmd.run:
    - name: echo "autoreply.yourdomain.com\tvacation:" > /etc/postfix/transport
    - require:
      - cmd: cp_vacation

postmap_transport:
  cmd.run:
    - name: postmap /etc/postfix/transport
    - require:
      - cmd: echo_transport

chown_vacation:
  cmd.run:
    - name: chown -R vacation:vacation /var/spool/vacation
    - require:
      - cmd: postmap_transport

echo_hosts:
  cmd.run:
    - name: echo "127.0.0.1 autoreply.yourdomain.com" >> /etc/hosts
    - require:
      - cmd: chown_vacation

mkdir_postfixadmin:
  cmd.run:
    - name: mkdir /etc/postfixadmin
    - require:
      - cmd: echo_hosts

/etc/postfixadmin/vacation.conf:
  file.managed:
    - source: salt://postfix/vacation.conf
    - template: jinja
    - require:
      - cmd: mkdir_postfixadmin
