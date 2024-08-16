# map-my-world
Project for management of locations of interest around the world

1) install fastapi:
pip install "fastapi[standard]"

2) install requirements
pip install requirements.txt

3) install postgreSQL 16

4) create database "mapmyworld" and substitute user and password in the SQLALCHEMY_DATABASE_URL variable in src/db/database.py

5) run:
    fastapi dev main.py
