get_postfixadmin:
  cmd.run:
    - name: wget http://sourceforge.net/projects/postfixadmin/files/latest/download

tar_postfixadmin:
  cmd.run:
    - name: tar -xzvf postfixadmin-2.3.6.tar.gz
    - require:
      - cmd: get_postfixadmin

mv_postfixadmin:
  cmd.run:
    - name: mv postfixadmin-2.3.6 /usr/share/postfixadmin
    - require:
      - cmd: tar_postfixadmin
