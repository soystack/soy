db4:
  pkg.installed:
    - pkgs:
      - db4
      - db4-devel
      - db4-utils

get_source:
  cmd.run:
    - name: wget https://pypi.python.org/packages/source/b/bsddb3/bsddb3-5.3.0.tar.gz#md5=d5aa4f293c4ea755e84383537f74be82 --no-check-certificate
    - require:
      - pkg: db4

tar_zxvf:
  cmd.run:
    - name: tar -zxvf bsddb3-5.3.0.tar.gz
    - require:
      - cmd: get_source

install_lib:
  cmd.run:
    - name: cd bsddb3-5.3.0 && python setup.py --berkeley-db=/usr/share/doc/db4-4.7.25/ build && python setup.py --berkeley-db=/usr/share/doc/db4-4.7.25/ install
    - require:
      - cmd: tar_zxvf
