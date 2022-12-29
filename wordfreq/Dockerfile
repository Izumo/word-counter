FROM registry.access.redhat.com/ubi8/python-38

RUN pip install flask requests jsonpickle

ADD WordFreq.py /opt/app-root/src
ADD run.sh /opt/app-root/src

CMD [ "/opt/app-root/src/run.sh" ]
