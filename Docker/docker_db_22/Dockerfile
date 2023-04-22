FROM mariadb:latest

ADD ./sql/script.sql /docker-entrypoint-initdb.d

ENV MYSQL_ROOT_PASSWORD admin 
ENV MYSQL_DATABASE LD01INFO01 
ENV MYSQL_USER admin 
ENV MYSQL_PASSWORD admin

RUN apt-get update && apt-get -y install vim

EXPOSE 3306

CMD ["mysqld"]
