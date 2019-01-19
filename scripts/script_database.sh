#!/bin/bash
# The script will fail at the first error encountered
set -e

sudo mysql << MYSQL_SCRIPT
CREATE DATABASE twitter;
USE twitter;
CREATE TABLE contacts (
    name VARCHAR(40) NOT NULL,
    url VARCHAR(40) NOT NULL,
    tweet_volume VARCHAR(40) NOT NULL);
MYSQL_SCRIPT
