FROM postgres:latest

WORKDIR .

ADD . /db

COPY init.sql /docker-entrypoint-initdb.d/