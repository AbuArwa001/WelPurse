#!/usr/bin/env bash
MYSQL_USER=WP_user_dev MYSQL_PWD=WP_db_pwd  MYSQL_HOST=localhost  MYSQL_DB=welpurse STORAGE_TYPE=db gunicorn --reload --bind 0.0.0.0:5001 'api.v1.app:app'