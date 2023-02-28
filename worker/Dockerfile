FROM python:3.6-alpine

RUN  pip3 install --upgrade redis jsonpickle requests flask pymongo

ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8

COPY worker-server.py /
WORKDIR /
# COPY worker-server.py ./

ENTRYPOINT	["python3", "worker-server.py"]