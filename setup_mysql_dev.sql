-- prepares a MySQL server for the project

CREATE USER IF NOT EXISTS 'WP_user_dev'@'localhost' IDENTIFIED BY 'WP_db_pwd';
GRANT ALL PRIVILEGES ON `welpurse`.* TO 'WP_user_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'WP_user_dev '@'localhost';
FLUSH PRIVILEGES;
