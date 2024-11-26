CREATE ROLE hive_user WITH LOGIN PASSWORD 'hive_password';
CREATE DATABASE metastore OWNER hive_user;
