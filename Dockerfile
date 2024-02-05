FROM python:3.12.0

COPY p2p_project /p2p_project
WORKDIR /p2p_project

RUN pip install -r /p2p_project/requirements.txt
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
