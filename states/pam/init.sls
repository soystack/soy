tools:
  pkg.installed:
    - pkgs:
      - gcc
      - make
      - autoconf

get_pam:
  {% set path = '/usr/local/src' %}
  cmd.run:
    - name: wget http://www.kernel.org/pub/linux/libs/pam/pre/library/Linux-PAM-0.77.tar.gz -P {{ path }}
    - require:
      - pkg: tools

tar_pam:
  cmd.run:
    - name: tar -zxvf {{ path }}/Linux-PAM-0.77.tar.gz -C {{ path }}
    - require:
      - cmd: get_pam

get_pwd:
  {% set path = path + '/Linux-PAM-0.77/modules' %}
  cmd.run:
    - name: wget http://cpbotha.net/files/pam_pwdfile/pam_pwdfile-0.99.tar.gz -P {{ path }}
    - require:
      - cmd: tar_pam

tar_pwd:
  {% set pam = path + '/pam_pwdfile-0.99.tar.gz' %}
  cmd.run:
    - name: tar -zxvf {{ pam }} -C {{ path }}
    - require:
      - cmd: get_pwd

del_def:
  {% set path = path.replace('/modules', '') %}
  cmd.run:
    - name: rm -f {{ path }}/default.defs
    - require:
      - cmd: tar_pwd

lnk_def:
  cmd.run:
    - name: ln -s {{ path }}/defs/redhat.defs {{ path }}/default.defs
    - require:
      - cmd: del_def

{% if grains['cpuarch'] == 'x86_64' %}
{{ path }}/configure.in:
  file.append:
    - source: salt://pam/configure.in
    - require:
      - cmd: lnk_def
{% endif %}

regen_conf:
  cmd.run:
    - name: cd {{ path }} && autoconf
    {% if grains['cpuarch'] == 'x86_64' %}
    - require:
      - file: {{ path }}/configure.in
    {% endif %}
    {% if grains['cpuarch'] == 'i686' %}
    - require:
      - cmd: lnk_def
    {% endif %}

make_all:
  cmd.run:
    - name: cd {{ path }} && make all
    - require:
      - cmd: regen_conf

copy_pam:
  cmd.run:
    {% if grains['cpuarch'] == 'x86_64' %}
      {% set lib = '/lib64' %}
    {% endif %}
    {% if grains['cpuarch'] == 'i686' %}
      {% set lib = '/lib' %}
    {% endif %}
    {% set path = path + '/modules/pam_pwdfile-0.99/pam_pwdfile.so' %}
    - name: cp {{ path }} {{ lib }}/security
    - require:
      - cmd: make_all
