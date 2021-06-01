FROM node as node-build
WORKDIR /web
COPY package.json yarn.lock ./
RUN yarn install

FROM python:3 as package
WORKDIR /web
ENV PYTHONUNBU FFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel -w /root/wheels -r requirements.txt


FROM python:3 as builder
ENV PYTHONUNBU FFERED 1

RUN apt-get update -y \
    && apt-get -f install \
    && apt-get upgrade -y \
    && apt-get clean \
    && pip install --upgrade pip

# Install packages
WORKDIR /web
COPY --from=package /root/wheels /root/wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/root/wheels -r requirements.txt

COPY . .

EXPOSE 3000