postfix:
  myhostname: mail.localdomain
  alias_maps: "hash:/etc/aliases"
  alias_database: "hash:/etc/aliases"
  myorigin: /etc/mailname
  mydestination: ""
  relayhost: ""
  mynetworks: "127.0.0.0/8 [::ffff:127.0.0.0]/104 [::1]/128"
  mailbox_size_limit: 0
  recipient_delimiter: "+"
  inet_interfaces: all
  virtual_alias_domains: ""
  virtual_alias_maps: "proxy:mysql:/etc/postfix/mysql-forwards.cf, mysql:/etc/postfix/mysql-email.cf"
  virtual_mailbox_domains: "proxy:mysql:/etc/postfix/mysql-domains.cf"
  virtual_mailbox_maps: "proxy:mysql:/etc/postfix/mysql-mailboxes.cf"
  virtual_mailbox_base: /home/vmail
  specified_group: postfix
  user: mailadmin
