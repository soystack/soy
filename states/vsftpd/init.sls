vsftpd:
  pkg.installed:
    - pkgs:
      - vsftpd
      - ftp
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
      - file: vsftpd
