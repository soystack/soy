base:
  nginx:
    - match: nodegroup
    - nginx
    - php-fpm
    - monit
    - vsftpd
    - pam
  mysql-slave:
    - match: nodegroup
    - mysql-slave
  mysql-master:
    - match: nodegroup
    - pdns
  powerdns:
    - match: nodegroup
    - pdns
  postfix:
    - match: nodegroup
    - postfix
    - dovecot
  vsftp:
    - match: nodegroup
    - vsftpd
  p3plpop09-v01.prod.phx3.secureserver.net:
    - match: nodegroup
    - postfix
  nfs-server:
    - match: nodegroup
    - nfs-server
  nfs-client:
    - match: nodegroup
    - nfs-client
