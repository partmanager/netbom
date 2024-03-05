FROM python:3.12-slim-bookworm

RUN apt update
RUN apt install make pylint graphviz -y

WORKDIR /mnt/netbom_backend/

ENV PYTHONPATH="/mnt/netbom_backend/src/"
COPY requirements-dev.txt /var/netbom_backend/
RUN pip install -r /var/netbom_backend/requirements-dev.txt
