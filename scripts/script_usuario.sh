#!/bin/bash
# The script will fail at the first error encountered
set -e

sudo mysql << MYSQL_SCRIPT
CREATE USER 'usuariocc'@'%' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON * . * TO 'usuariocc'@'%' WITH GRANT OPTION;
MYSQL_SCRIPT
