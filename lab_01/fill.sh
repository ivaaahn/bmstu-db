#!/usr/bin/zsh

psql < ./scripts/create_tables.sql
psql < ./scripts/fill_db.sql