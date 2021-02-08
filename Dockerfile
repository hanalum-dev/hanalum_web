FROM python:3
MAINTAINER shinkeonkim <singun11@kookmin.ac.kr>
ENV PYTHONUNBUFFERED 1
WORKDIR /web
COPY . .
RUN pip install -r requirements.txt