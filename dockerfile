FROM apache/airflow:latest
USER root
RUN mkdir -p /usr/share/man/man1
RUN apt-get update && apt-get install -y default-jdk && apt-get clean
USER airflow