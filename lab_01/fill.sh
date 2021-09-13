#!/usr/bin/zsh

psql < create_db.sql
psql < fill_db.sql