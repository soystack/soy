server {
    listen 80;
    server_name .{{ host }};
    access_log /var/www/{{ user }}/{{ host }}/logs/access.log;
    error_log /var/www/{{ user }}/{{ host }}/logs/error.log;
    root /var/www/{{ user }}/{{ host }}/htdocs;

    index index.html index.php;

    location ~ \.php$ {
        fastcgi_pass 127.0.0.1:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
