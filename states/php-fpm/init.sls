php-fpm:
  pkg:
    - installed
  service:
    - running
    - enable: True
    - require:
        - pkg: php-fpm
