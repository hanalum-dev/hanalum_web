FROM python:3
MAINTAINER shinkeonkim singun11@kookmin.ac.kr
ENV PYTHONUNBU  FFERED 1
WORKDIR /web
COPY . .
RUN apt-get update -y
RUN apt-get upgrade -y
RUN pip install -r requirements.txt