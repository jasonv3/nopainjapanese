# 阿里云部署（Debian 10）
## mysql
```
  // buster (stable) (database) 1.0.5: MySQL database server
  apt-get install default-mysql-server

  systemctl start mariadb.service

  systemctl enable mariadb.service

  mysql_secure_installation
```