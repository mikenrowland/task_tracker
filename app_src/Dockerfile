FROM python:3.10.1

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update

WORKDIR /app_src

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN adduser --disabled-password --gecos '' mykie

RUN chown -R mykie:mykie /app_src

USER mykie