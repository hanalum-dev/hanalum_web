FROM python:3 as package
WORKDIR /web
ENV PYTHONUNBU FFERED 1

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel -w /root/wheels -r requirements.txt


FROM python:3 as builder
ENV PYTHONUNBU FFERED 1
WORKDIR /web
COPY . .

RUN apt-get update -y \
    && apt-get -f install \
    && apt-get upgrade -y \
    && apt-get clean \
    && pip install --upgrade pip

RUN apt-get install -y nodejs npm
RUN npm install
RUN npm run build

COPY --from=package /root/wheels /root/wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/root/wheels -r requirements.txt

EXPOSE 3000