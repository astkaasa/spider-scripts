server {
  listen 80 backlog=4096;
  listen [::]:80;

  server_name example.com;

  root /home/ubuntu;
  index index.html;
  charset utf-8;
  location / {
  }

  location /manage {
    proxy_pass http://127.0.0.1:8080;
    auth_basic "Restricted Content";
    auth_basic_user_file /etc/nginx/.htpasswd;
  }

  location /data {
    auth_basic "Restricted Content";
    auth_basic_user_file /etc/nginx/.htpasswd;
    autoindex on;
    try_files $uri $uri/ =404;
  }

  location /t/ {
    secure_link $arg_md5,$arg_expires;
    secure_link_md5 "$secure_link_expires$uri Spectre";
    if ($secure_link = "") { return 403; }
    if ($secure_link = "0") { return 410; }
  }
}
