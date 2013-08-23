postfix:
  soft_bounce: yes
  mail_owner: postfix
  setgid_group: postdrop
  delay_warning_time: 4
  html_directory: no
  command_directory: /usr/sbin
  daemon_directory: /usr/libexec/postfix
  queue_directory: /var/spool/postfix
  sendmail_path: /usr/sbin/sendmail.postfix
  newaliases_path: /usr/bin/newaliases.postfix
  mailq_path: /usr/bin/mailq.postfix
  manpage_directory: /usr/share/man
  inet_interfaces: all
  mydomain: yourdomain.com
  myhostname: host.yourdomain.com
  mynetworks: "$config_directory/mynetworks"
  mydestination: "$myhostname, localhost.$mydomain, localhost"
  relay_domains: "proxy:mysql:/etc/postfix/mysql-relay_domains_maps.cf"
  recipient_delimiter: + 
  alias_maps: "hash:/etc/aliases"
  alias_database: "hash:/etc/aliases"
  transport_maps: "hash:/etc/postfix/transport"
  local_recipient_maps: ""
  virtual_alias_maps: "proxy:mysql:/etc/postfix/mysql-virtual_alias_maps.cf, regexp:/etc/postfix/virtual_regexp"
  virtual_mailbox_base: /home/vmail
  virtual_mailbox_domains: "proxy:mysql:/etc/postfix/mysql-virtual_domains_maps.cf"
  virtual_mailbox_maps: "proxy:mysql:/etc/postfix/mysql-virtual_mailbox_maps.cf"
  virtual_mailbox_limit_maps: "proxy:mysql:/etc/postfix/mysql-virtual_mailbox_limit_maps.cf"
  virtual_minimum_uid: 101
  virtual_uid_maps: static:101
  virtual_gid_maps: static:12
  virtual_transport: dovecot
  dovecot_destination_recipient_limit: 1
  debug_peer_level: 2
  debugger_command: "PATH=/bin:/usr/bin:/usr/local/bin:/usr/X11R6/bin\nxxgdb $daemon_directory/$process_name $process_id & sleep 5"
  smtpd_sasl_auth_enable: yes
  smtpd_sasl_security_options: noanonymous
  smtpd_sasl_local_domain: $myhostname
  broken_sasl_auth_clients: yes
  smtpd_sasl_type: dovecot
  smtpd_sasl_path: private/auth
  smtp_use_tls: yes
  smtpd_use_tls: yes 
  smtpd_tls_security_level: may
  smtpd_tls_loglevel: 1
  smtpd_tls_received_header: yes
  smtpd_tls_session_cache_timeout: 3600s
  tls_random_source: "dev:/dev/urandom"
  smtp_tls_session_cache_database: "btree:$data_directory/smtp_tls_session_cache"
  # Change mail.example.com.* to your host name 
  smtpd_tls_key_file: /etc/pki/tls/private/mail.example.com.key
  smtpd_tls_cert_file: /etc/pki/tls/certs/mail.example.com.crt
  smtpd_tls_CAfile: /etc/pki/tls/root.crt
  smtpd_client_restrictions: ""
  smtpd_helo_restrictions: ""
  smtpd_sender_restrictions: ""
  smtpd_recipient_restrictions:
    >permit_sasl_authenticated, 
    permit_mynetworks, 
    reject_unauth_destination,
    reject_non_fqdn_sender,
    reject_non_fqdn_recipient, 
    reject_unknown_recipient_domain,
    reject_rbl_client zen.spamhaus.org,
    reject_rbl_client bl.spamcop.net,
    reject_rbl_client dnsbl.sorbs.net

  smtpd_helo_required: yes
  unknown_local_recipient_reject_code: 550
  disable_vrfy_command: yes
  smtpd_data_restrictions: reject_unauth_pipelining

  # Other	options
  # email	size limit ~20Meg
  message_size_limit: 204800000
