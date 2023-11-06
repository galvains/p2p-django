FROM python:3.12.0

COPY p2p_project /p2p_project
WORKDIR /p2p_project
EXPOSE 8000


RUN pip install -r /p2p_project/requirements.txt
RUN adduser --disabled-password galvains

USER galvains