## Allow local private IP to connect to local mysql server

```mysql
CREATE USER '<user>'@'<private ip>' IDENTIFIED BY '<password>';
GRANT ALL PRIVILEGES ON database_name.* TO 'nodeuser'@'<private ip>';
SHOW GRANTS FOR '<user>'@'<private ip>';
FLUSH PRIVILEGES;
```

```mysql
GRANT ALL PRIVILEGES ON hotel_cms.* TO 'nodeuser'@'192.168.3.106' IDENTIFIED BY 'password123';
FLUSH PRIVILEGES;
```