FROM python:3.7-alpine

RUN apk add gcc libffi-dev musl-dev tzdata

RUN echo UTC > /etc/timezone && \
    ln -sf /usr/share/zoneinfo/UTC /etc/localtime

ADD requirements.txt /
RUN pip install -r requirements.txt

ADD bot.py /

ENTRYPOINT ["python"]
CMD ["bot.py"]