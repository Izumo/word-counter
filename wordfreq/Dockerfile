FROM registry.access.redhat.com/ubi8/python-38

RUN pip install fastapi uvicorn aiohttp

ADD WordFreq.py /opt/app-root/src
ADD run.sh /opt/app-root/src

CMD [ "/opt/app-root/src/run.sh" ]
